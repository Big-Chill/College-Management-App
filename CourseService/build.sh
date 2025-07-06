#!/bin/bash

IMAGE_NAME="course-service"

echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .
