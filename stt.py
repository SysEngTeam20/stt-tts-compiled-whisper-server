from faster_whisper import WhisperModel

# Load the model (options: "tiny", "base", "small", "medium", "large-v2")
model = WhisperModel("base", device="cpu")  # Use "cuda" if you have GPU

# Transcribe audio
segments, info = model.transcribe("output.wav")

# Print transcription with timestamps
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}") 