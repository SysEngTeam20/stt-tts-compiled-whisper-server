from fastapi import FastAPI, UploadFile, File, WebSocket
from faster_whisper import WhisperModel
from whisperspeech.pipeline import Pipeline
import torchaudio
from pathlib import Path
from fastapi.responses import FileResponse
import uvicorn
import numpy as np
from typing import Dict

app = FastAPI()

# Store active connections
stt_connections: Dict[str, WebSocket] = {}
tts_connections: Dict[str, WebSocket] = {}

@app.websocket("/stt/ws/{client_id}")
async def websocket_stt_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    stt_connections[client_id] = websocket
    try:
        while True:
            # Receive audio data as bytes
            audio_data = await websocket.receive_bytes()
            
            # Convert to numpy array and transcribe
            audio_np = np.frombuffer(audio_data, dtype=np.float32)
            segments, info = whisper_model.transcribe(audio_np)
            text = " ".join([segment.text for segment in segments])
            
            # Send back transcription
            await websocket.send_json({"text": text})
    except Exception as e:
        print(f"Error in STT websocket: {e}")
    finally:
        del stt_connections[client_id]

@app.websocket("/tts/ws/{client_id}")
async def websocket_tts_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    tts_connections[client_id] = websocket
    try:
        while True:
            # Receive text
            data = await websocket.receive_json()
            text = data["text"]
            
            # Generate audio
            audio_tensor = tts_model.generate(text)
            
            # Convert to bytes and send
            audio_data = audio_tensor.cpu().numpy().tobytes()
            await websocket.send_bytes(audio_data)
    except Exception as e:
        print(f"Error in TTS websocket: {e}")
    finally:
        del tts_connections[client_id]

# Initialize models
whisper_model = WhisperModel("base", device="cpu")
tts_model = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-tiny-en+pl.model')

@app.post("/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as buffer:
        content = await audio.read()
        buffer.write(content)
    
    # Transcribe
    segments, info = whisper_model.transcribe(temp_path)
    
    # Collect all text
    text = " ".join([segment.text for segment in segments])
    
    # Clean up
    Path(temp_path).unlink()
    
    return {"text": text}

@app.post("/tts")
async def text_to_speech(text: str):
    # Generate audio
    audio_tensor = tts_model.generate(text)
    
    # Save audio
    output_path = "output.wav"
    torchaudio.save(output_path, audio_tensor.cpu(), 24000)
    
    # Return audio file
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="generated_speech.wav"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001) 