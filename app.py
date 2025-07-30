import io
from flask import Flask, request, Response, render_template_string
from PIL import Image
import numpy as np
import potrace

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html>
      <head><title>PNG → SVG</title></head>
      <body>
        <h1>Upload a PNG to vectorize</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
          <p><input type="file" name="image" accept="image/png" required></p>
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

    # 1) Load image & grayscale
    threshold = int(request.form.get("threshold", 128))
    img = Image.open(request.files["image"].stream).convert("L")

    # 2) Binarize to 1-bit (0 or 255)
    bw = img.point(lambda x: 0 if x < threshold else 255, "1")

    # 3) Convert to numpy array of 0/1
    arr = np.array(bw, dtype=np.uint8)
    # Potrace expects bits: 1=black, 0=white
    bmp = potrace.Bitmap(arr)

    # 4) Trace to get a Path object
    PATH = bmp.trace(turdsize=20, alphamax=1.0, opttolerance=0.2)

    # 5) Generate SVG string
    svg_header = (
        '<?xml version="1.0" standalone="no"?>\n'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" '
        '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n'
    )
    svg_body = PATH.to_svg()
    svg = svg_header + svg_body

    return Response(svg, mimetype="image/svg+xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)), debug=True)
