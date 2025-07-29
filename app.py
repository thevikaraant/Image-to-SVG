from flask import Flask, request, jsonify, send_file
import base64
import cv2
import numpy as np
from PIL import Image
import potrace
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_svg():
    try:
        data = request.json
        if 'image' not in data:
            return jsonify({'error': 'Missing image field'}), 400

        # Decode base64 image
        image_data = data['image']
        image_bytes = base64.b64decode(image_data)

        # Convert to OpenCV image
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_GRAYSCALE)

        # Threshold image (binarize)
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        # Encode to BMP for potrace
        _, bmp_bytes = cv2.imencode('.bmp', thresh)
        bmp_stream = io.BytesIO(bmp_bytes.tobytes())
        bmp_image = Image.open(bmp_stream)

        # Create bitmap for potrace
        bitmap = potrace.Bitmap(np.array(bmp_image).astype(np.uint8))
        path = bitmap.trace()

        # Create SVG
        svg_io = io.StringIO()
        svg_io.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n')
        for curve in path:
            svg_io.write('<path d="M ')
            start_point = curve.start_point
            svg_io.write(f"{start_point[0]} {start_point[1]} ")
            for segment in curve:
                if isinstance(segment, potrace.Curve):
                    c = segment.c
                    svg_io.write(f"C {c[0][0]} {c[0][1]}, {c[1][0]} {c[1][1]}, {c[2][0]} {c[2][1]} ")
                else:
                    end_point = segment.end_point
                    svg_io.write(f"L {end_point[0]} {end_point[1]} ")
            svg_io.write('Z" fill="black"/>\n')
        svg_io.write('</svg>')

        svg_data = svg_io.getvalue()
        svg_b64 = base64.b64encode(svg_data.encode()).decode()

        return jsonify({
            'status': 'success',
            'format': 'SVG',
            'svg_base64': svg_b64
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
