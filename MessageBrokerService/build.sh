#!/bin/bash

# Name of the Docker image
IMAGE_NAME="message-broker-service"

echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .
