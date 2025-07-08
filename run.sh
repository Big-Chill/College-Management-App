#!/bin/bash

echo "Starting all services with Docker Compose..."
docker-compose up -d --build

echo "All services are starting in the background."
echo "User Service:    http://localhost:8000/docs"
echo "Course Service:  http://localhost:8001/docs"
echo "Message Broker Service: http://localhost:8002/docs"
