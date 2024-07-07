import json

import numpy
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory, Response
#from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
# from Routers import Api,
from flask_cors import CORS
import os
import datetime
import re
from measurement import process_image
import mmcv
from mmdet.apis import init_detector, inference_detector
import numpy as np
# import takeimage
from flask_socketio import SocketIO, emit
import cv2 as cv
import pyrealsense2 as rs
import uuid

from flask_cors import CORS
# from flask_mysqldb import MySQL
# from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os
import requests
# import datetime
# import models

# # .env 환경변수 사용
# from dotenv import load_dotenv


# migrate = Migrate()
# cors = CORS()





app = Flask(__name__)
CORS(app)
# socketio= SocketIO(app)

# Global variables
pipelines = []
align = None


# Add Database
# MySQL DB

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://DoJunKwon:smartfarm@localhost:3306/sensor_db' # mysql://username:password@localhost:3306/db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'DoJunKwon'
# app.config['MYSQL_PASSWORD'] = 'smartfarm'
# app.config['MYSQL_DB'] = 'sensor_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
mysql = MySQL(app)
# api = Api(app)

IMAGE_FOLDER = r'D:\UOA2\2024Sem1\COMPSYS 700\p4p\All_image\Original' #r'D:\UOA2\2024Sem1\COMPSYS 700\Test\takeimage\server'
RESULT_IMAGE = r'D:\UOA2\2024Sem1\COMPSYS 700\p4p\All_image\Result'
    #r'D:\UOA2\2024Sem1\COMPSYS 700\p4p\main\Project 22_ Plant monitoring system for Smart Farm_\Compendium Andy\mmdetection\resultImage'

IMAGE_DIRECTORY = r'D:\UOA2\2024Sem1\COMPSYS 700\p4p\All_image\Original'
SAVE_DIRECTORY = r'D:\UOA2\2024Sem1\COMPSYS 700\p4p\All_image\Result'

config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
# config_file = r'D:\UOA2\2024Sem1\COMPSYS 700\backend\mmdetection\mmdetection\configs\mask_rcnn\mask-rcnn_r50_fpn_1x_coco.py'
#config_file = 'mmdetection/configs/mask_rcnn/mask-rcnn_r50_fpn_1x_coco.py' #'configs/mask_rcnn/mask-rcnn_r50_fpn_1x_coco.py'
# download the checkpoint from model zoo and put it in `checkpoints/`
# url: https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth
checkpoint_file = 'models/laboro_tomato_big_48ep.pth'
model = init_detector(config_file, checkpoint_file, device='cpu')  # initialize the object detection model on cpu
# Create a model
class environments(db.Model):
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

@app.route('/')
def welcome():
    return "<h1>Welcome to Smart Farm</h1>"

@app.route('/api/data', methods=['GET'])
def get_data():
    datas = environments.query.all()
    result = environments_schema.dump(datas)
    return jsonify(result)

@app.route('/api/data/<id>', methods=['GET'])
def get_data_by_id(id):
    datas = environments.query.get(id)
    return environment_schema.jsonify(datas)

@app.route('/api/data/<datetime>', methods=['GET'])
def get_data_by_date(datetime):
    datas = environments.query.filter_by(date=datetime).all()
    return jsonify(datas)

@app.route('/api/data/count', methods=['GET'])
def get_data_count():
    count = environments.query.count()
    return jsonify(count)



#************ Image AI generate function **************#
def process():
    # model = init_detector(config_file, checkpoint_file, device='cpu')  # initialize the object detection model on cpu

    # Get all image and depth files.
    image_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.png')]
    depth_files = [f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.npy')]

    # image_files = sorted([f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.png')])
    # depth_files = sorted([f for f in os.listdir(IMAGE_DIRECTORY) if f.endswith('.npy')])

    assert len(image_files) == len(depth_files), "Mismatch in number of image and depth files"
    colors = [
        (250, 10, 10),  # Green color for "rippned" label
        (255, 165, 0),  # Orange color for "half_ripened" label
        (0, 163, 24)  # Red color for "green" label
    ]

    results = []
    for i in range(len(image_files)):
        imagePath = os.path.join(IMAGE_DIRECTORY, image_files[i])
        depthPath = os.path.join(IMAGE_DIRECTORY, depth_files[i])
        img = mmcv.imread(imagePath)
        # model = init_detector(config_file, checkpoint_file,
        #                       device='cpu')  # initialize the object detection model on cpu
        depthData = np.load(depthPath)  # load numpy array
        result = inference_detector(model,
                                    img)  # to perform object detection inference on input image using initialized model. i
        # it will return detection result which include bounding box coordinate and segmentation mask.
        # show_result_pyplot(model, img, result)

        bbox_result, segm_result = result
        # Ensure results are concatenated properly
        # bbox_result, segm_result = result if isinstance(result, tuple) else (result, None)

        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(bbox_result)
        ]
        labels = np.concatenate(labels)
        bboxes = np.vstack(bbox_result)

        # if segm_result:
        #     segm_result = [x for x in segm_result if x != []]
        #     if segm_result:
        #         segment = np.vstack(segm_result)
        #     else:
        #         segment = np.array([])
        # else:
        #     segment = np.array([])

        # Modify the segmentation mask colors based on labels
        if segm_result:
            for label, segms in zip(range(len(segm_result)), segm_result):
                color = colors[label]
                for segm in segms:
                    if isinstance(segm, np.ndarray):
                        mask = segm.astype(bool)
                        img[mask] = img[mask] * 0.5 + np.array(color) * 0.5

        # segm_result = [x for x in segm_result if x != []]
        # segment = np.vstack(segm_result)


        out_file = f'{SAVE_DIRECTORY}/result_{i+1}.png'
        # print(bboxes)
        model.show_result(img, result, out_file=out_file ,mask_color=colors)


@app.route('/api/process', methods=['GET'])
def process_endpoint():
    try:
        results = process()
        return jsonify({"message": "Processing completed", "results": results}), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500





def convert_json_keys_and_values(json_str, quote_type="'"):
    # Replace double quotes with single quotes for keys
    def replace_keys(match):
        return f"{quote_type}{match.group(1)}{quote_type}:"

    def replace_values(match):
        return f": {quote_type}{match.group(1)}{quote_type}"

    # Replace double quotes with single quotes for keys
    json_str = re.sub(r'"(\w+)":', replace_keys, json_str)

    json_str = re.sub(r':\s*"([^"]*)"', replace_values, json_str)

    return json_str

@app.route('/save_json', methods=['GET'])
def save_json():
    datas = environments.query.all()
    result = environments_schema.dump(datas)
    # convert datas as list of dictionary
    data_dict = [dict(row) for row in result]

    # convert to json
    data_json = json.dumps(data_dict, default=str)

    # Convert JSON keys to single quotes or remove quotes
    ts_content = convert_json_keys_and_values(data_json)

    # Generate TypeScript file content
    ts_content = f"export default iotData = {ts_content};"

    #save local drive
    with open('data.json', 'w') as json_file:
        json_file.write(data_json)

    with open('data_dict.txt', 'w') as dict_file:
        dict_file.write(str(data_dict))

    with open('iotData.ts', 'w') as ts_file:
        ts_file.write(ts_content)

    return jsonify({"message": "TS Data saved successfully"}), 200

@app.route('/images', methods=['GET'])
def get_folder():
    images = os.listdir(IMAGE_FOLDER)
    print(f"Image list: {images}")
    return jsonify(images)


@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    print(f"Requested image: {filename}")
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/result', methods=['GET'])
def get_folder2():
    images = os.listdir(RESULT_IMAGE)
    print(f"Image list: {images}")
    return jsonify(images)

@app.route('/result2/<filename>', methods=['GET'])
def get_image2(filename):
    print(f"Requested image: {filename}")
    return send_from_directory(RESULT_IMAGE, filename)










if __name__ == '__main__': # Script executed directly?
    # app.run(debug=True) # Launch built-in web server and run this Flask web app
    # serials, ctx = findDevices()
    # enableDevices(serials, ctx, 1280, 720, 15)
    # socketio.run(app,host='127.0.0.1',port= 5000, debug=True)
    app.run(debug=True)
