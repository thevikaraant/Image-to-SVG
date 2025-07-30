import os
import io
import subprocess
from flask import Flask, request, Response, render_template_string
from PIL import Image

app = Flask(__name__)

@app.route("/")
def index():
    # Simple upload form so you can test in-browser
    return render_template_string("""
    <!doctype html>
    <html>
      <head>
        <title>PNG to SVG Converter</title>
      </head>
      <body>
        <h1>PNG → SVG Converter</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
          <p>
            <label>PNG File:
              <input type="file" name="image" accept="image/png" required>
            </label>
          </p>
          <p>
            <label>Threshold (0–255):
              <input type="number" name="threshold" min="0" max="255" value="128">
            </label>
          </p>
          <p><button type="submit">Convert to SVG</button></p>
        </form>
      </body>
    </html>
    """)

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return "No image uploaded", 400
    upload = request.files["image"]

    # 1) Load and convert to grayscale
    threshold = int(request.form.get("threshold", 128))
    img = Image.open(upload.stream).convert("L")

    # 2) Binarize to 1‑bit
    bw = img.point(lambda x: 0 if x < threshold else 255, "1")

    # 3) Convert 1‑bit to RGB and save as PPM in-memory
    ppm_buf = io.BytesIO()
    bw.convert("RGB").save(ppm_buf, format="PPM")
    pnm_data = ppm_buf.getvalue()

    # 4) Invoke Potrace to output an SVG
    proc = subprocess.run(
        [
          "potrace",
          "-s",                # SVG output
          "--turdsize", "20",  # despeckle small islands
          "--alphamax", "1.0", # corner smoothing
          "--opttolerance", "0.2",  # path optimization
          "--output", "-"      # send SVG to stdout
        ],
        input=pnm_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    # 5) Return SVG to client
    return Response(proc.stdout, mimetype="image/svg+xml")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
