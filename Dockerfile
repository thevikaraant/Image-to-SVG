# Use a slim Python base image
FROM python:3.10-slim

# Prevent creation of .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# Install Potrace and libpng for Pillow
RUN apt-get update \
    && apt-get install -y --no-install-recommends potrace libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE ${PORT}

# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
