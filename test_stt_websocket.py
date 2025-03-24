import asyncio
import websockets
import wave
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_stt_websocket():
    # Connect to WebSocket
    uri = "ws://localhost:5001/stt/ws/test_client"
    async with websockets.connect(uri) as websocket:
        logger.info("Connected to STT WebSocket")

        # Read an existing WAV file
        audio_path = "output.wav"  # Make sure this file exists
        if not Path(audio_path).exists():
            logger.error(f"Please create a test_audio.wav file with actual speech")
            return

        # Read the WAV file
        with open(audio_path, "rb") as f:
            wav_data = f.read()
        
        logger.info(f"Sending {len(wav_data)} bytes of WAV data")
        await websocket.send(wav_data)
        logger.info("Audio data sent, waiting for response...")

        # Get response
        response = await websocket.recv()
        result = json.loads(response)
        logger.info(f"Received transcription: {result['text']}")

        # Close properly
        await websocket.close()

if __name__ == "__main__":
    asyncio.run(test_stt_websocket()) 