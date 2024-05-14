import json
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from Routers import Api, resource
from flask_cors import CORS
import os
import datetime

from flask_cors import CORS
# from flask_mysqldb import MySQL
# from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import os
# import datetime
# from models import environments

# # .env 환경변수 사용
# from dotenv import load_dotenv


# migrate = Migrate()
# cors = CORS()


# load_dotenv()
# DB_NAME = "database.db"

# x = datetime.datetime.now() # show current date and time

# this is the sample of the code to show image

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes
#
# SERVER_FOLDER = 'server'
# if not os.path.exists(SERVER_FOLDER):
#     os.makedirs(SERVER_FOLDER)
#
#
# @app.route('/png')
# def get_png():
#     # Assuming you have the PNG file stored locally in the 'server' folder
#     png_path = os.path.join(SERVER_FOLDER, '1_color.png')
#     # Send the PNG file as a response
#     return send_file(png_path, mimetype='image/png')
#
#
# if __name__ == '__main__':
#     app.run(host='localhost', port=5000, debug=True)
#



app = Flask(__name__)
CORS(app)


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
api = Api(app)


# Create a model
class environments(db.Model):
    __tablename__ = 'environments'
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



# @app.route('/api/data', methods=['POST'])
# def useradd():
#     temperature = request.json['temperature']


# @app.route('/api/data', methods=['GET'])
# def get_data():
#     try:
#         conn = mysql.connection
#         if conn is None:
#             return "No connection" ,500
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM environments")
#         data = cur.fetchall()
#         cur.close()
#
#         # # serialize data to json
#         # json_data = json.dumps(data)
#         #
#         # # save as json file
#         # with open(r'D:\UOA2\2024Sem1\COMPSYS 700\backend\data.json', 'w') as f:
#         #     f.write(json_data)
#
#         return jsonify(data)
#     except Exception as e:
#         return str(e), 500




# @app.route('/sensor')
# def sensor():
#     return render_template('sensor.html')
#
# @app.route('/all')
# def select_all():
#     City = city.query.all()
#     return render_template('db.html', City=City)


# @app.route('/')
# def mainpage():  # show main page
#     return render_template()
#
# basdir = os.path.abspath(os.path.dirname(__file__))
# dbfile = os.path.join(basdir, 'db.sqlite')
#
#
#
#
# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html', name=name)
#
# @app.route('/connect', methods=['GET', 'POST'])
# def connect():
#     if request.method == 'POST':
#         user = request.form['user']
#         password = request.form['password']
#         print(user, password)
#         return render_template('connect.html', user=user, password=password)
#
#     return render_template('connect.html')


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404







if __name__ == '__main__': # Script executed directly?
    app.run(debug=True) # Launch built-in web server and run this Flask web app
