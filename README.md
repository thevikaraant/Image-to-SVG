# Vectorizer.ai PNG to SVG Converter

This Flask application sends PNG images to Vectorizer.ai for vectorization and returns the resulting SVG.

## Setup

1. Clone the repository.
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set environment variables:

   ```
   export VECTORIZER_API_ID=vk45avcji4qanbd
   export VECTORIZER_API_SECRET=ah79opbc8889rl6dnktkrmov6mhe8ur8nt55sli6ujcgh8umdo69
   export PORT=5000
   ```

4. Run locally:

   ```
   gunicorn --bind 0.0.0.0:$PORT app:app
   ```

## Docker

Build and run with Docker:

```
docker build -t vectorizer-converter .
docker run -e VECTORIZER_API_ID=$VECTORIZER_API_ID \
           -e VECTORIZER_API_SECRET=$VECTORIZER_API_SECRET \
           -p 5000:5000 \
           vectorizer-converter
```

## Usage

- **Browser**: Visit `http://localhost:5000/` to upload a PNG.
- **cURL**:

  ```
  curl -u "$VECTORIZER_API_ID:$VECTORIZER_API_SECRET" \
       -F "image=@your.png" \
       http://localhost:5000/convert > result.svg
  ```
