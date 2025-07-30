FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Install system packages including dev headers for potrace
RUN apt-get update && apt-get install -y --no-install-recommends \
    potrace \
    libpotrace-dev \
    libpng-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .
EXPOSE ${PORT}
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
