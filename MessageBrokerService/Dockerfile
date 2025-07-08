# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Set environment variable for uvicorn to find the app
ENV MODULE_NAME=app.main
ENV VARIABLE_NAME=app

# Command to run the app with live reload (for development, remove --reload for production)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
