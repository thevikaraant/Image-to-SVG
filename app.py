import os
import requests
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

API_ID = os.environ.get("VECTORIZER_API_ID", "")
API_SECRET = os.environ.get("VECTORIZER_API_SECRET", "")
VECTORIZE_URL = "https://vectorizer.ai/api/v1/vectorize"

@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html>
      <head><title>PNG → SVG via Vectorizer.ai</title></head>
      <body>
        <h1>PNG to SVG Converter</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
          <p><input type="file" name="image" accept="image/png" required></p>
          <p><button type="submit">Convert</button></p>
        </form>
      </body>
    </html>
    """)

@app.route("/convert", methods=["POST"])
def convert():
    f = request.files.get("image")
    if not f:
        return "No file uploaded", 400

    resp = requests.post(
        VECTORIZE_URL,
        auth=(API_ID, API_SECRET),
        files={"image": f.stream}
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        return f"Vectorizer.ai error: {e}", resp.status_code

    return Response(resp.content, mimetype="image/svg+xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
