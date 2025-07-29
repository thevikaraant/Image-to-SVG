import os
from flask import Flask, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "PNG to SVG Converter is Live"

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return "No file part", 400
    file = request.files["image"]
    if file.filename == "":
        return "No selected file", 400

    # Dummy placeholder for actual conversion logic
    img = Image.open(file.stream)
    img = img.convert("L")  # simulate processing

    output = io.BytesIO()
    img.save(output, format="PNG")  # You'd normally output an SVG
    output.seek(0)
    return send_file(output, mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 👈 Use Render's expected port
    app.run(host="0.0.0.0", port=port, debug=True)  # 👈 Bind to 0.0.0.0
