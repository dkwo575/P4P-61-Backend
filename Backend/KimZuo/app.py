import os
from flask import Flask, request, jsonify
from database import *
from upload.upload_plot import *

app = Flask(__name__)
database_directory = database_directory = os.path.join(os.getcwd(), "database", "farm_data.json")
data = database_read(database_directory)


# # Set GET POST request through methods
# @app.route('/args', methods=["POST"])
# def args_request():
#     # Receive and process GET POST data requests
#     temperature_get = request.args.get('temperature')
#     fluorescents_get = request.args.get('fluorescents_get')
#
#     print("temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get))
#
#     return "temperature = %s, fluorescents = %s" % (temperature_get, fluorescents_get)


#
# upload_plot.py relate
#

# Route for updating or adding plot area
@app.route('/args/update_or_add_plot_area', methods=['POST'])
def update_or_add_area():
    request_data = request.get_json()
    farm_id = request_data.get('farm_id')
    building_id = request_data.get('building_id')
    plot_id = request_data.get('plot_id')
    plot_date = request_data.get('plot_date')
    new_plot_area = request_data.get('new_plot_area')

    # Call the function to update or add plot area
    success = update_or_add_plotArea(data, farm_id, building_id, plot_id, plot_date, new_plot_area)

    return jsonify({'success': success})


# Route for updating or adding plot fruitlets
@app.route('/args/update_or_add_plot_fruitlets', methods=['POST'])
def update_or_add_fruitlets():
    request_data = request.get_json()
    farm_id = request_data.get('farm_id')
    building_id = request_data.get('building_id')
    plot_id = request_data.get('plot_id')
    plot_date = request_data.get('plot_date')
    new_plot_fruitlets = request_data.get('new_plot_fruitlets')

    # Call the function to update or add plot fruitlets
    success = update_or_add_plotFruitlets(data, farm_id, building_id, plot_id, plot_date, new_plot_fruitlets)

    return jsonify({'success': success})


# Similarly, create routes for updating or adding plot volume and width

if __name__ == '__main__':
    app.run(debug=True)
