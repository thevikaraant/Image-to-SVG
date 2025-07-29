from flask import Flask, request, send_file, render_template_string
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_FORM = '''
<!doctype html>
<title>PNG to SVG Converter</title>
<h1>Upload a PNG to convert to SVG</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Convert>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.png'):
            filename = secure_filename(file.filename)
            png_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(png_path)

            pbm_path = png_path.replace('.png', '.pbm')
            svg_path = png_path.replace('.png', '.svg')

            subprocess.run(['convert', png_path, pbm_path], check=True)
            subprocess.run(['potrace', pbm_path, '-s', '-o', svg_path], check=True)

            return send_file(svg_path, as_attachment=True)
    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)