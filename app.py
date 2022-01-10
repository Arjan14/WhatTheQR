from flask import Flask, redirect, url_for, render_template, request, send_file
from flask_cors import CORS
import qrcode
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/make")
def make():
    return render_template("make.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    buffer = BytesIO()
    data = request.form.get('data')

    img = qrcode.make(data)
    img.save(buffer)
    buffer.seek(0)

    response = send_file(buffer, mimetype='image/png')
    return response



if __name__ == '__main__':
    app.run()
