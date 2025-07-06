#!/bin/bash

# Name of the Docker image and container
IMAGE_NAME="user-service"
CONTAINER_NAME="user-service-container"

# Stop and remove any existing container with the same name
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "Running Docker container: $CONTAINER_NAME"
docker run --env-file .env -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
