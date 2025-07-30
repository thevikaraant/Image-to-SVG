# PNG to SVG Converter

This Flask application converts PNG images to SVG vector format using Potrace.

## Features

- Configurable black-and-white threshold for vector tracing
- Potrace flags for despeckling, corner smoothing, and path optimization
- In-memory processing (no temporary files)

## Requirements

- Python 3.10+
- Potrace CLI installed

### Python dependencies
Install via pip:
```
pip install -r requirements.txt
```

## Usage

### Endpoints
- **GET /**  
  Health check; returns `PNG to SVG Converter is Live`.
- **POST /convert**  
  Convert PNG to SVG.  
  - Form fields:  
    - `image` – the PNG file to convert (multipart/form-data)  
    - `threshold` (optional) – integer between 0 and 255 for binarization threshold (default: 128)

### Example
```
curl -X POST -F "image=@your.png" -F "threshold=150" https://<your-domain>/convert > output.svg
```

## Deployment

### Docker
```
docker build -t png2svg .
docker run -p 10000:10000 png2svg
```

### Render.com
1. Add `Dockerfile` and `.dockerignore` (included).  
2. Push to Git.  
3. Create a Web Service on Render, select Docker.  
4. Access `https://<service>.onrender.com/convert`.

## Potrace Flags
- `--turdsize 20` – removes speckles smaller than 20 pixels  
- `--alphamax 1.0` – smoothing parameter for corners  
- `--opttolerance 0.2` – tolerance for path optimization  
