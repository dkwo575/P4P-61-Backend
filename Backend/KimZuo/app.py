from flask import Flask, request
import os
from database import *
from upload_farm import *

app = Flask(__name__)
database_directory = os.getcwd() + "/database"
write_file_path = database_directory + "\\test.txt"


# Set GET POST request through methods
@app.route('/args', methods=["GET", "POST"])
def args_request():
    # Receive and process GET POST data requests
    temperature_get = request.args.get('temperature')
    fluorescents_get = request.args.get('fluorescents_get')

    print("temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get))
    newdata_join(temperature_get, fluorescents_get)
    return "temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get)
