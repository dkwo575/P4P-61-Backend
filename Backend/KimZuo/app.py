from flask import Flask, request
import json

app = Flask(__name__)


# Set GET request through methods
@app.route('/args', methods=["GET"])
def args_request():
    # Receive and process GET data requests
    user_name = request.args.get('user_name')
    user_age = request.args.get('user_age')

    print("user_name = %s, user_age = %s" % (user_name, user_age))

    return "user_name = %s, user_age = %s" % (user_name, user_age)
