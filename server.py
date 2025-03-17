from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
from whisperspeech.pipeline import Pipeline
import torchaudio
from pathlib import Path
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()

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