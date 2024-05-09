from flask import *
from flask_cors import CORS
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

SERVER_FOLDER = 'server'
if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)

Last_File = ''


@app.route('/png')
def get_png():
    global Last_File
    print(Last_File)
    if not Last_File:
        print("No PNG file available")
        # return "No PNG file available"
        file_path = os.path.join(SERVER_FOLDER, "1_color.png")
        print(file_path)
        return send_file(file_path, mimetype='image/png')

    if not os.path.exists(Last_File):
        print("PNG file not found")
        return "PNG file not found"

    return send_file(Last_File, mimetype='image/png')


@app.route('/upload_png', methods=['POST'])
def upload_png():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)  # Secure the filename to prevent directory traversal
        file_path = os.path.join(SERVER_FOLDER, filename)
        file.save(file_path)
        global Last_File
        Last_File = file_path  # Update the Last_File variable
        print(Last_File)
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
