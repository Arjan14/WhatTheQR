from io import BytesIO
import os
import qrcode
from flask import Flask, redirect, url_for, render_template, request, send_file, abort, send_from_directory
from flask_cors import CORS
import imghdr
from werkzeug.utils import secure_filename

#startup of app
app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

#validation of images
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

#app route for root page (index)
@app.route("/")
def home():
    return render_template("index.html")

#app route of learn page
@app.route("/learn")
def learn():
    return render_template("learn.html")

#app route of make page
@app.route("/make")
def make():
    return render_template("make.html")

#app route of uploadfile
@app.route("/uploadfile")
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template("upload.html", files=files)

#app route of generating qr code
@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    buffer = BytesIO()
    data = request.form.get('data')

    img = qrcode.make(data)
    img.save(buffer)
    buffer.seek(0)

    response = send_file(buffer, mimetype='image/png')
    return response

#app route of uploading file
@app.route('/uploadfile', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))

#app route of saving the uploaded files
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

#flask run
if __name__ == '__main__':
    app.run()
