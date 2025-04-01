#!/bin/bash

# Exit on error
set -e

# Configuration
IMAGE_NAME="compiled-whisper"
IMAGE_TAG="latest"
REGISTRY="your-registry"  # Change this to your registry

# Build Docker image
echo "Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f deploy/docker/Dockerfile .

# Tag image for registry
echo "Tagging image for registry..."
docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

# Push to registry (uncomment when ready to push)
# echo "Pushing image to registry..."
# docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -k deploy/k8s

echo "Deployment complete!"
echo "To check the status, run:"
echo "  kubectl get pods"
echo "  kubectl get services" 