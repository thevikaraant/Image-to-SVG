import io, os, subprocess
from flask import Flask, request, Response
from PIL import Image
import numpy as np
import potrace

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return "No image uploaded", 400
    # load sketch PNG
    img = Image.open(request.files["image"].stream).convert("L")
    # binarize
    bw = img.point(lambda x: 0 if x < 128 else 255, "1")
    arr = np.array(bw, dtype=np.uint8)
    bmp = potrace.Bitmap(arr)
    path = bmp.trace(turdsize=20, alphamax=1.0, opttolerance=0.2)
    svg = '<?xml version="1.0"?>\n' + path.to_svg()
    return Response(svg, mimetype="image/svg+xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
