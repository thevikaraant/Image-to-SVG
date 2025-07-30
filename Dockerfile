# Dockerfile for PNG to SVG Converter
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y potrace libpng-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
ENV PORT 10000
EXPOSE 10000

# Start application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
