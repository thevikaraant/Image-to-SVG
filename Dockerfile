# Use a slim Python base
FROM python:3.10-slim

# Don’t buffer Python stdout/stderr and skip .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

# Install Potrace (no extra recommends) and libpng for Pillow
RUN apt-get update \
    && apt-get install -y --no-install-recommends potrace libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code last to leverage Docker cache on deps
COPY . .

# Expose the port
EXPOSE ${PORT}

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
