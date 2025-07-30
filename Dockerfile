# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Don’t write .pyc files, and make stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install Potrace CLI and libpng for Pillow
RUN apt-get update && \
    apt-get install -y --no-install-recommends potrace libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app.py .

# Tell Docker (and Render) which port we listen on
EXPOSE 5000

# Use shell form so $PORT is expanded at container startup
CMD gunicorn --bind "0.0.0.0:$PORT" app:app
