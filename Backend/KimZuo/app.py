from flask import Flask, request
import os
from database import *

app = Flask(__name__)
current_directory = os.getcwd()
database_directory = os.getcwd() + "/database"
write_file_path = database_directory + "\\test.txt"

# Set GET POST request through methods
@app.route('/args', methods=["GET", "POST"])
def args_request():
    # Receive and process GET POST data requests
    user_name = request.args.get('user_name')
    user_age = request.args.get('user_age')

    print("user_name = %s, user_age = %s" % (user_name, user_age))
    newdata_join(user_name, user_age)
    return "user_name = %s, user_age = %s" % (user_name, user_age)
