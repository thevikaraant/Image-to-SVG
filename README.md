# PNG to SVG Converter

This Flask application converts PNG images to SVG vector format using Potrace.

## Features

- Configurable black-and-white threshold for vector tracing
- Potrace flags for despeckling (`turdsize`), corner smoothing (`alphamax`), and path optimization (`opttolerance`)
- In-memory PPM conversion to avoid Pillow's PBM limitations
- Simple HTML upload form at `/` for browser testing

## Files

- **app.py** – The Flask application
- **Dockerfile** – Docker build instructions (installs Potrace)
- **Aptfile** – For Render Python Buildpack (installs Potrace & libpng-dev)
- **requirements.txt** – Python dependencies
- **build.sh** – Manual install script for local environments
- **runtime.txt** – Python runtime version for buildpacks
- **README.md** – This documentation

## Usage

### 1. Docker

```bash
docker build -t png2svg .
docker run -p 10000:10000 png2svg
curl -X POST -F "image=@your.png" -F "threshold=128" \
     http://localhost:10000/convert > output.svg
```

### 2. Render Python Buildpack

Push to Render with `Aptfile` present:
- Render installs system packages from `Aptfile`
- Then runs standard Python buildpack

### 3. Browser Upload

Visit `http://<host>/` to test via the simple HTML form.

## Example

```bash
curl -X POST -F "image=@your.png" -F "threshold=150" \
     https://<your-domain>/convert > result.svg
```
