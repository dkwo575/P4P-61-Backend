from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

SERVER_FOLDER = 'server'
if not os.path.exists(SERVER_FOLDER):
    os.makedirs(SERVER_FOLDER)

SERVER_ORIGINAL_FOLDER = 'server/Original'
if not os.path.exists(SERVER_ORIGINAL_FOLDER):
    os.makedirs(SERVER_ORIGINAL_FOLDER)

SERVER_RESULT_FOLDER = 'server/Result'
if not os.path.exists(SERVER_RESULT_FOLDER):
    os.makedirs(SERVER_RESULT_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    client_id = request.form.get('client_id', 'unknown')  # Extract client_id from form data

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        if client_id == 'realsense_client':
            file_path = os.path.join(SERVER_ORIGINAL_FOLDER, filename)
        elif client_id == 'ai_client':
            file_path = os.path.join(SERVER_RESULT_FOLDER, filename)
        else:
            file_path = os.path.join(SERVER_FOLDER, filename)
        file.save(file_path)
        file_type = filename.split('.')[-1].upper()  # Extract file type

        print(f"Uploaded file: {filename}, Type: {file_type}, Client: {client_id}")

        notify_clients('File uploaded', filename, file_type, client_id)

        return jsonify({'message': 'File uploaded successfully', 'file_type': file_type, 'client_id': client_id})
    else:
        return jsonify({'error': 'Upload failed'})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Traverse the server folder to find the file
    for root, dirs, files in os.walk(SERVER_FOLDER):
        if filename in files:
            file_path = os.path.join(root, filename)
            return send_file(file_path)

    # Return an error if the file is not found
    return jsonify({'error': 'File not found'})


@app.route('/api/process', methods=['GET'])
def send_files_to_ai():
    try:
        # Get all image and depth files.
        image_files = [f for f in os.listdir(SERVER_ORIGINAL_FOLDER) if f.endswith('.png')]
        depth_files = [f for f in os.listdir(SERVER_ORIGINAL_FOLDER) if f.endswith('.npy')]

        if len(image_files) != len(depth_files):
            return jsonify({"message": "Mismatch in number of image and depth files"}), 400

        # Emit each file to the AI client
        for image_file, depth_file in zip(image_files, depth_files):
            image_file_path = os.path.join(SERVER_ORIGINAL_FOLDER, image_file)
            depth_file_path = os.path.join(SERVER_ORIGINAL_FOLDER, depth_file)

            # Create download URLs for the files
            server_address = request.host_url.rstrip('/')
            image_download_url = f"{server_address}/download/{image_file}"
            depth_download_url = f"{server_address}/download/{depth_file}"
            print(image_download_url)
            print(depth_download_url)

            # Emit the URLs to the AI client
            file_dumps(image_file, image_download_url, depth_file, depth_download_url)

        return jsonify({"message": "Files sent to AI client successfully"}), 200

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'message': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


def notify_clients(event, filename, file_type, client_id):
    server_address = request.host_url.rstrip('/')
    download_url = f"{server_address}/download/{filename}"
    socketio.emit('update', {
        'event': event,
        'filename': filename,
        'download_url': download_url,
        'file_type': file_type,
        'client_id': client_id  # Include client_id in the notification
    })
    print(
        f"Notification sent to all clients: {event} - {filename} - Download URL: {download_url} - Client ID: {client_id}")


def file_dumps(image_file, image_download_url, depth_file, depth_download_url):
    socketio.emit('send_file_to_ai', {
        'image_file': image_file,
        'image_download_url': image_download_url,
        'depth_file': depth_file,
        'depth_download_url': depth_download_url
    })
    print(
        f"Notification sent to all AI clients: Image_file: {image_file} - Depth_file: {depth_file}")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
