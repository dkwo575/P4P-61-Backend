import os
import json
import re
import uuid
import datetime
import numpy as np
import cv2 as cv
import mmcv
import requests
import pyrealsense2 as rs
from flask import Flask, request, jsonify, send_file, send_from_directory, Response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from mmdet.apis import init_detector, inference_detector

# Initialize Flask app and extensions
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DoJunKwon:smartfarm@localhost:3306/sensor_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize folders
SERVER_FOLDER = 'server'
SERVER_ORIGINAL_FOLDER = os.path.join(SERVER_FOLDER, 'Original')
SERVER_RESULT_FOLDER = os.path.join(SERVER_FOLDER, 'Result')
os.makedirs(SERVER_FOLDER, exist_ok=True)
os.makedirs(SERVER_ORIGINAL_FOLDER, exist_ok=True)
os.makedirs(SERVER_RESULT_FOLDER, exist_ok=True)

# Image directories for processing
IMAGE_DIRECTORY = SERVER_ORIGINAL_FOLDER
SAVE_DIRECTORY = SERVER_RESULT_FOLDER

# Object detection model configuration
config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
checkpoint_file = 'models/laboro_tomato_big_48ep.pth'
model = init_detector(config_file, checkpoint_file, device='cpu')


# Database model and schema
class Environments(db.Model):
    __tablename__ = 'real_iot'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float(100))
    humidity = db.Column(db.Float(100))
    light = db.Column(db.Float(100))
    waterLevel = db.Column(db.Float(100))
    soilHumidity = db.Column(db.Float(100))
    steam = db.Column(db.Float(100))
    datetime = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, temperature, humidity, light, waterLevel, soilHumidity, steam, datetime):
        self.temperature = temperature
        self.humidity = humidity
        self.light = light
        self.waterLevel = waterLevel
        self.soilHumidity = soilHumidity
        self.steam = steam
        self.datetime = datetime


class DataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'temperature', 'humidity', 'light', 'waterLevel', 'soilHumidity', 'steam', 'datetime')


environment_schema = DataSchema()
environments_schema = DataSchema(many=True)


# Routes and API endpoints
@app.route('/')
def welcome():
    return "<h1>Welcome to Smart Farm</h1>"


@app.route('/api/data', methods=['GET'])
def get_data():
    datas = Environments.query.all()
    result = environments_schema.dump(datas)
    return jsonify(result)


@app.route('/api/data/<id>', methods=['GET'])
def get_data_by_id(id):
    data = Environments.query.get(id)
    return environment_schema.jsonify(data)


@app.route('/api/data/count', methods=['GET'])
def get_data_count():
    count = Environments.query.count()
    return jsonify(count)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    client_id = request.form.get('client_id', 'unknown')

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    if client_id == 'realsense_client':
        file_path = os.path.join(SERVER_ORIGINAL_FOLDER, filename)
    elif client_id == 'ai_client':
        file_path = os.path.join(SERVER_RESULT_FOLDER, filename)
    else:
        file_path = os.path.join(SERVER_FOLDER, filename)
    file.save(file_path)
    file_type = filename.split('.')[-1].upper()

    print(f"Uploaded file: {filename}, Type: {file_type}, Client: {client_id}")

    notify_clients('File uploaded', filename, file_type, client_id)
    return jsonify({'message': 'File uploaded successfully', 'file_type': file_type, 'client_id': client_id})


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    for root, dirs, files in os.walk(SERVER_FOLDER):
        if filename in files:
            file_path = os.path.join(root, filename)
            return send_file(file_path)
    return jsonify({'error': 'File not found'})


@app.route('/images', methods=['GET'])
def get_folder():
    images = os.listdir(IMAGE_DIRECTORY)
    return jsonify(images)


@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(IMAGE_DIRECTORY, filename)


@app.route('/result', methods=['GET'])
def get_folder2():
    images = os.listdir(SAVE_DIRECTORY)
    return jsonify(images)


@app.route('/result2/<filename>', methods=['GET'])
def get_image2(filename):
    return send_from_directory(SAVE_DIRECTORY, filename)


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/process', methods=['GET'])
def process_endpoint():
    try:
        results = process_images()
        return jsonify({"message": "Processing completed", "results": results}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def process_images():
    image_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.png')]
    depth_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.npy')]
    assert len(image_files) == len(depth_files), "Mismatch in number of image and depth files"
    results = []

    for i in range(len(image_files)):
        image_path = os.path.join(IMAGE_DIRECTORY, image_files[i])
        depth_path = os.path.join(IMAGE_DIRECTORY, depth_files[i])
        img = mmcv.imread(image_path)
        depth_data = np.load(depth_path)
        result = inference_detector(model, img)
        bbox_result, segm_result = result
        labels = [np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(bbox_result)]
        labels = np.concatenate(labels)
        bboxes = np.vstack(bbox_result)
        segment = np.vstack(segm_result) if segm_result else np.array([])

        out_file = os.path.join(SAVE_DIRECTORY, f'result_{i + 1}.png')
        model.show_result(img, result, out_file=out_file)

        results.append({
            'image': image_files[i],
            'depth': depth_files[i],
            'bboxes': bboxes.tolist(),
            'labels': labels.tolist(),
            'segment': segment.tolist() if segment.size > 0 else [],
            'result_image': f'result_{i + 1}.png'
        })

    return results


def gen_frames():
    while True:
        frame = get_frame()
        if frame:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def get_frame():
    global pipelines, align
    for (device, pipe) in pipelines:
        frames = pipe.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not aligned_depth_frame or not color_frame:
            continue
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.03), cv.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))
        _, buffer = cv.imencode('.jpg', images)
        return buffer.tobytes()
    return None


def notify_clients(event, filename, file_type, client_id):
    server_address = request.host_url.rstrip('/')
    download_url = f"{server_address}/download/{filename}"
    socketio.emit('update', {
        'event': event,
        'filename': filename,
        'download_url': download_url,
        'file_type': file_type,
        'client_id': client_id
    })
    print(
        f"Notification sent to all clients: {event} - {filename} - Download URL: {download_url} - Client ID: {client_id}")


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('response', {'message': 'Connected to server'})


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
