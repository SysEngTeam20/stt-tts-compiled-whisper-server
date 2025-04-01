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
git clone https://github.com/SysEngTeam20/compiled-whisper-server.git
cd compiled-whisper-server
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

## Deployment Strategies

This section covers different deployment options for the Compiled Whisper application.

### Docker Deployment

1. Create a Dockerfile:
```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download model file (if not included in repository)
RUN curl -L "https://liveuclac-my.sharepoint.com/:u:/g/personal/zcababr_ucl_ac_uk/EX-K9-PVdlhKkP1IJchp84UB7Qoe5d1vjMKzeriQ2Rwgaw?e=MIE0Tj" -o s2a-q4-hq-fast-en%2Bpl.model

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "server.py"]
```

2. Build the Docker image:
```bash
docker build -t compiled-whisper .
```

3. Run the container:
```bash
docker run -p 5001:5001 compiled-whisper
```

### Kubernetes Deployment

1. Create a Kubernetes deployment manifest (`k8s/deployment.yaml`):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: compiled-whisper
spec:
  replicas: 2
  selector:
    matchLabels:
      app: compiled-whisper
  template:
    metadata:
      labels:
        app: compiled-whisper
    spec:
      containers:
      - name: compiled-whisper
        image: your-registry/compiled-whisper:latest
        ports:
        - containerPort: 5001
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: model-storage
          mountPath: /app/s2a-q4-hq-fast-en%2Bpl.model
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: compiled-whisper
spec:
  selector:
    app: compiled-whisper
  ports:
  - port: 80
    targetPort: 5001
  type: LoadBalancer
```

2. Create a PersistentVolume for the model file (`k8s/pv.yaml`):
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: model-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  hostPath:
    path: "/data/model"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
```

3. Apply the Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

### IBM Cloud Deployment

1. Install IBM Cloud CLI and Kubernetes plugin:
```bash
# Install IBM Cloud CLI
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh

# Install Kubernetes plugin
ibmcloud plugin install container-service
```

2. Log in to IBM Cloud:
```bash
ibmcloud login
```

3. Create a Kubernetes cluster (if not exists):
```bash
ibmcloud ks cluster create classic --name compiled-whisper-cluster --zone us-south
```

4. Get cluster credentials:
```bash
ibmcloud ks cluster config --cluster compiled-whisper-cluster
```

5. Create a Container Registry namespace:
```bash
ibmcloud cr namespace-add compiled-whisper
```

6. Build and push Docker image to IBM Container Registry:
```bash
# Tag the image
docker tag compiled-whisper us.icr.io/compiled-whisper/compiled-whisper:latest

# Log in to IBM Container Registry
ibmcloud cr login

# Push the image
docker push us.icr.io/compiled-whisper/compiled-whisper:latest
```

7. Deploy to Kubernetes:
```bash
# Update the image in deployment.yaml to use IBM Container Registry
# Then apply the Kubernetes manifests
kubectl apply -f k8s/
```

8. Monitor the deployment:
```bash
kubectl get pods
kubectl get services
```

### Scaling and Monitoring

1. **Horizontal Pod Autoscaling**
Add to your deployment:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: compiled-whisper-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: compiled-whisper
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

2. **IBM Cloud Monitoring**
- Enable IBM Cloud Monitoring with Prometheus
- Set up Grafana dashboards for visualization
- Configure alerts for resource usage and errors

### Security Considerations

1. **Network Security**
- Use IBM Cloud Security Groups
- Configure Network Policies in Kubernetes
- Enable TLS/SSL with IBM Cloud Certificate Manager

2. **Access Control**
- Use IBM Cloud IAM for authentication
- Implement RBAC in Kubernetes
- Secure API endpoints with API keys or OAuth

3. **Data Security**
- Use IBM Cloud Key Protect for secrets
- Enable encryption at rest
- Regular security updates and patches

### Cost Optimization

1. **Resource Management**
- Use IBM Cloud Cost Estimator
- Implement resource quotas
- Monitor and adjust resource limits

2. **Storage Optimization**
- Use IBM Cloud Object Storage for model files
- Implement caching strategies
- Regular cleanup of temporary files

For more detailed information about IBM Cloud deployment, refer to the [IBM Cloud Documentation](https://cloud.ibm.com/docs). 