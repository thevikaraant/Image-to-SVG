import os
import io
import subprocess
from flask import Flask, request, Response
from PIL import Image

app = Flask(__name__)

@app.route("/")
def index():
    return "PNG to SVG Converter is Live"

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return "No image uploaded", 400
    upload = request.files["image"]

    # Configurable black-white threshold (0-255)
    threshold = int(request.form.get("threshold", 128))
    img = Image.open(upload.stream).convert("L")
    img = img.point(lambda x: 0 if x < threshold else 255, "1")  # 1-bit image

    # Save as PBM in memory
    pbm_io = io.BytesIO()
    img.save(pbm_io, format="PBM")
    pbm_data = pbm_io.getvalue()

    # Call Potrace with despeckling, corner smoothing, and optimization
    proc = subprocess.run(
        ["potrace", "-s", "--turdsize", "20", "--alphamax", "1.0", "--opttolerance", "0.2", "--output", "-"],
        input=pbm_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    svg_bytes = proc.stdout
    return Response(svg_bytes, mimetype="image/svg+xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
