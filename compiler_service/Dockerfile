FROM python:3.10-slim

# Install system dependencies for compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    g++ \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install django gunicorn requests

# Expose app port
EXPOSE 8000

# Run with Gunicorn (multi-worker, high timeout)
CMD ["gunicorn", "compiler_service.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
