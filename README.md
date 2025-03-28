# Compiled Whisper

A high-performance speech-to-text and text-to-speech server built with FastAPI, featuring WebSocket support for real-time audio processing. This project combines the power of Faster Whisper for speech recognition and WhisperSpeech for text-to-speech synthesis.

## Features

- **Real-time Speech-to-Text (STT)**
  - WebSocket-based streaming audio transcription
  - HTTP endpoint for file-based transcription
  - Powered by Faster Whisper model
  - Support for various audio formats

- **Real-time Text-to-Speech (TTS)**
  - WebSocket-based streaming audio synthesis
  - HTTP endpoint for text-to-speech conversion
  - Powered by WhisperSpeech model
  - High-quality audio output (48kHz sample rate)

- **Technical Features**
  - FastAPI-based REST API
  - WebSocket support for real-time communication
  - CORS enabled for cross-origin requests
  - Comprehensive logging system
  - Audio resampling and format conversion
  - Error handling and connection management

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/compiled-whisper.git
cd compiled-whisper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the server with:
```bash
python server.py
```

The server will start on `http://localhost:5001` by default.

### API Endpoints

#### WebSocket Endpoints

1. **Speech-to-Text WebSocket**
   - URL: `ws://localhost:5001/stt/ws/{client_id}`
   - Accepts raw PCM audio data
   - Returns JSON with transcribed text

2. **Text-to-Speech WebSocket**
   - URL: `ws://localhost:5001/tts/ws/{client_id}`
   - Accepts JSON with text to synthesize
   - Returns raw PCM audio data

#### HTTP Endpoints

1. **Speech-to-Text**
   - URL: `POST http://localhost:5001/stt`
   - Accepts WAV audio file
   - Returns JSON with transcribed text

2. **Text-to-Speech**
   - URL: `POST http://localhost:5001/tts`
   - Accepts text string
   - Returns WAV audio file

### Testing

A test script is provided to demonstrate WebSocket functionality:

```bash
python test_stt_websocket.py
```

## Audio Specifications

- Input audio for STT: 48kHz sample rate, 16-bit PCM, mono
- Output audio from TTS: 48kHz sample rate, 16-bit PCM, mono
- Automatic resampling is performed when needed

## Dependencies

Key dependencies include:
- FastAPI
- Faster Whisper
- WhisperSpeech
- Uvicorn
- NumPy
- SciPy
- Torch
- TorchAudio

For a complete list of dependencies, see `requirements.txt`.

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Acknowledgments

- [Faster Whisper](https://github.com/guillaumekln/faster-whisper)
- [WhisperSpeech](https://github.com/collabora/WhisperSpeech)
- [FastAPI](https://fastapi.tiangolo.com/)

## Building Executables

This project can be compiled into standalone executables for macOS, Windows, and Linux using PyInstaller.

### Prerequisites for Building

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Download the required model file:
   - Download the WhisperSpeech model file `s2a-q4-hq-fast-en+pl.model` from:
     [UCL SharePoint Link](https://liveuclac-my.sharepoint.com/:u:/g/personal/zcababr_ucl_ac_uk/EX-K9-PVdlhKkP1IJchp84UB7Qoe5d1vjMKzeriQ2Rwgaw?e=MIE0Tj)
   - Place it in the project root directory
   - Note: The file will be downloaded with URL-encoded name `s2a-q4-hq-fast-en%2Bpl.model`, which is fine

3. For macOS:
   - Xcode Command Line Tools
   - For Apple Silicon support: macOS 11.0 or later

4. For Windows:
   - Visual C++ Build Tools (optional, for better compatibility)

5. For Linux:
   - GCC and development libraries
   - For Ubuntu/Debian:
     ```bash
     sudo apt-get install build-essential
     ```

### Building the Executable

1. Ensure you have the model file `s2a-q4-hq-fast-en+pl.model` in the project root directory
2. Run the build script:
```bash
python build.py
```

2. The compiled executable will be created in the `dist/compiled_whisper_[platform]` directory:
   - macOS: `dist/compiled_whisper_darwin/compiled_whisper`
   - Windows: `dist/compiled_whisper_windows/compiled_whisper.exe`
   - Linux: `dist/compiled_whisper_linux/compiled_whisper`

### Running the Compiled Application

1. Navigate to the appropriate platform directory in `dist/`
2. Run the executable:
   - macOS/Linux: `./compiled_whisper`
   - Windows: `compiled_whisper.exe`

The server will start on `http://localhost:5001` by default.

### Notes

- The compiled executable includes the necessary model files
- The first launch might take longer as it extracts resources
- For macOS, you might need to right-click and select "Open" the first time to bypass security
- For Windows, you might need to allow the application through Windows Defender 