from flask import Flask, send_file, request
from flask_cors import CORS
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

SERVER_FOLDER = 'server'
if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)

# Global variable to hold the current PNG file path
current_png_file = None


@app.route('/png')
def get_png():
    global current_png_file
    if current_png_file is None or not os.path.exists(current_png_file):
        return "No PNG file available"
    return send_file(current_png_file, mimetype='image/png')


@app.route('/upload_png', methods=['POST'])
def upload_png():
    global current_png_file
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(SERVER_FOLDER, filename)
        file.save(file_path)
        current_png_file = file_path
        return 'PNG file uploaded successfully'


@app.route('/upload_array', methods=['POST'])
def upload_array():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file.save(os.path.join(SERVER_FOLDER, file.filename))
        return 'NumPy array file uploaded successfully'


@app.route('/download_png/<filename>', methods=['GET'])
def download_png(filename):
    return send_file(os.path.join(SERVER_FOLDER, filename), mimetype='image/png')


@app.route('/download_array/<filename>', methods=['GET'])
def download_array(filename):
    return send_file(os.path.join(SERVER_FOLDER, filename), mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
