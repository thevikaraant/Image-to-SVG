# Sketch PNG to SVG Converter

This Flask application converts a sketch PNG into an SVG using Python-Potrace.

## Endpoint

**POST /convert**

- Form field: `image` – sketch PNG upload.

## Local Usage

```bash
pip install -r requirements.txt
python app.py
# or
gunicorn --bind 0.0.0.0:5000 app:app
```

## Docker

```bash
docker build -t sketch-to-svg .
docker run -e PORT=5000 -p 5000:5000 sketch-to-svg
```

## Deploy on Render

1. Create a new Web Service with Docker.
2. Connect your repo; Render auto-detects Dockerfile.
3. Deploy and test POST /convert.
