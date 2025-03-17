import torch
from pathlib import Path
from whisperspeech.pipeline import Pipeline
import torchaudio

# Initialize the pipeline with English model
tts_pipe = Pipeline(s2a_ref='collabora/whisperspeech:s2a-q4-tiny-en+pl.model')

# Generate speech
text = "This is a test sentence."
try:
    # Generate audio tensor
    audio_tensor = tts_pipe.generate(text)
    
    # Convert to numpy array and save
    output_path = Path("output.wav")
    torchaudio.save(output_path, audio_tensor.cpu(), 24000)
    print(f"Audio saved to {output_path.absolute()}")

except Exception as e:
    print(f"Error: {str(e)}")
    print("Install required packages with:")
    print("pip install whisperspeech torchaudio")