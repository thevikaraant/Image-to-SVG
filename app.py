import os
import io
import subprocess
from flask import Flask, request, send_file, abort
from PIL import Image

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return "No image uploaded", 400
    # Load image and convert to grayscale + binarize
    img = Image.open(request.files["image"].stream).convert("L")
    bw = img.point(lambda x: 0 if x < 128 else 255, "1")
    # Save to PBM via PPM (avoid Pillow PBM issue)
    ppm_buf = io.BytesIO()
    bw.convert("RGB").save(ppm_buf, format="PPM")
    ppm_data = ppm_buf.getvalue()
    # Call Potrace CLI
    try:
        proc = subprocess.run(
            ["potrace", "-s", "--turdsize", "20", "--alphamax", "1.0",
             "--opttolerance", "0.2", "--output", "-"],
            input=ppm_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except FileNotFoundError:
        abort(500, description="Potrace CLI not installed")
    svg_bytes = proc.stdout
    return send_file(
        io.BytesIO(svg_bytes),
        mimetype="image/svg+xml",
        as_attachment=False,
        download_name="output.svg"
    )

@app.route("/")
def index():
    return "Sketch-to-SVG service is live"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
