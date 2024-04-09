import os
from flask import Flask, request
from database import *

app = Flask(__name__)
database_directory = os.getcwd() + "/database"
write_file_path = database_directory + "\\test.txt"


# Set GET POST request through methods
@app.route('/args', methods=["POST"])
def args_request():
    # Receive and process GET POST data requests
    temperature_get = request.args.get('temperature')
    fluorescents_get = request.args.get('fluorescents_get')

    print("temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get))

    return "temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get)
