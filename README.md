# Sketch PNG to SVG Converter (CLI-based)

This Flask service converts a sketch PNG into an SVG by using the Potrace CLI.

## Endpoints

- **GET /**: health check  
- **POST /convert**: convert sketch PNG to SVG  
  - Form field: `image` (PNG file upload)  

## Setup

### Requirements
- Python 3.10+
- Docker (for container deployment)

### Installation

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
python app.py
# or with Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app
```

### Docker

Build and run:

```bash
docker build -t sketch-to-svg-cli .
docker run -e PORT=5000 -p 5000:5000 sketch-to-svg-cli
```

### Deploy on Render

1. Create a new Web Service, selecting **Docker**.  
2. Connect your GitHub repo containing this project.  
3. Render will use the Dockerfile to build and expose `$PORT`.  
4. Send POST requests to `/convert`.
