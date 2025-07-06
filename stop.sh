#!/bin/bash

echo "Stopping and removing all Docker Compose containers..."
docker-compose down

echo "All services have been stopped and removed."
