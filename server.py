from fastapi import FastAPI, UploadFile, File, WebSocket
from faster_whisper import WhisperModel
from whisperspeech.pipeline import Pipeline
import torchaudio
from pathlib import Path
from fastapi.responses import FileResponse
import uvicorn
import numpy as np
from typing import Dict
import logging
from datetime import datetime
import wave
from fastapi import WebSocketDisconnect
import io
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Store active connections
stt_connections: Dict[str, WebSocket] = {}
tts_connections: Dict[str, WebSocket] = {}

@app.websocket("/stt/ws/{client_id}")
async def websocket_stt_endpoint(websocket: WebSocket, client_id: str):
    try:
        await websocket.accept()
        stt_connections[client_id] = websocket
        logger.info(f"STT Client connected: {client_id}")
        
        while True:
            try:
                audio_data = await websocket.receive_bytes()
                logger.info(f"STT Request from {client_id}:")
                logger.info(f"  └─ Received audio: {len(audio_data)} bytes")
                
                # Convert raw PCM to WAV
                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(48000)
                    wav_file.writeframes(audio_data)
                
                # Save temporary WAV file
                temp_path = f"temp_{client_id}.wav"
                with open(temp_path, "wb") as f:
                    f.write(wav_buffer.getvalue())
                
                try:
                    # Transcribe from file
                    logger.info(f"Processing audio file: {temp_path}")
                    segments, info = whisper_model.transcribe(temp_path)
                    
                    # Convert generator to list before joining
                    segments_list = list(segments)  # Convert generator to list
                    text = " ".join([segment.text for segment in segments_list])
                    
                    # Log the actual transcription result
                    logger.info(f"Transcription result: '{text}' ({len(segments_list)} segments)")
                    
                    if not text.strip():
                        text = "[No speech detected]"
                    
                    # Send back transcription and log the response
                    response = {"text": text}
                    await websocket.send_json(response)
                    logger.info(f"STT Response sent to {client_id}:")
                    logger.info(f"  └─ Transcribed text: {text}")
                    
                except Exception as e:
                    logger.error(f"Transcription error: {str(e)}")
                    await websocket.send_json({"error": str(e)})
                finally:
                    # Clean up
                    if Path(temp_path).exists():
                        Path(temp_path).unlink()
                    
            except WebSocketDisconnect:
                logger.info(f"Client {client_id} disconnected")
                break
                
    except Exception as e:
        logger.error(f"STT Error for {client_id}: {str(e)}")
        logger.exception("Full traceback:")
    finally:
        if client_id in stt_connections:
            del stt_connections[client_id]
        logger.info(f"STT Client disconnected: {client_id}")

@app.websocket("/tts/ws/{client_id}")
async def websocket_tts_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    tts_connections[client_id] = websocket
    logger.info(f"TTS Client connected: {client_id}")
    try:
        while True:
            # Receive text
            data = await websocket.receive_json()
            text = data["text"]
            logger.info(f"TTS Request from {client_id}:")
            logger.info(f"  └─ Input text: {text}")
            
            # Generate audio
            audio_tensor = tts_model.generate(text)
            
            # Convert to bytes and send
            audio_data = audio_tensor.cpu().numpy().tobytes()
            await websocket.send_bytes(audio_data)
            logger.info(f"TTS Response to {client_id}:")
            logger.info(f"  └─ Generated audio: {len(audio_data)} bytes")
    except Exception as e:
        logger.error(f"TTS Error for {client_id}: {str(e)}")
    finally:
        del tts_connections[client_id]
        logger.info(f"TTS Client disconnected: {client_id}")

# Initialize models
whisper_model = WhisperModel("base", device="cpu")
tts_model = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-tiny-en+pl.model')

@app.post("/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    logger.info(f"HTTP STT Request:")
    logger.info(f"  └─ File: {audio.filename} ({audio.content_type})")
    
    # Save uploaded file temporarily
    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as buffer:
        content = await audio.read()
        buffer.write(content)
    
    # Transcribe
    segments, info = whisper_model.transcribe(temp_path)
    text = " ".join([segment.text for segment in segments])
    
    # Clean up
    Path(temp_path).unlink()
    
    logger.info(f"HTTP STT Response:")
    logger.info(f"  └─ Transcribed text: {text}")
    return {"text": text}

@app.post("/tts")
async def text_to_speech(text: str):
    logger.info(f"HTTP TTS Request:")
    logger.info(f"  └─ Input text: {text}")
    
    # Generate audio
    audio_tensor = tts_model.generate(text)
    
    # Save audio
    output_path = "output.wav"
    torchaudio.save(output_path, audio_tensor.cpu(), 24000)
    
    logger.info(f"HTTP TTS Response:")
    logger.info(f"  └─ Generated audio file: {output_path}")
    
    # Return audio file
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="generated_speech.wav"
    )

if __name__ == "__main__":
    logger.info("Starting server on port 5001...")
    uvicorn.run(app, host="0.0.0.0", port=5001) 