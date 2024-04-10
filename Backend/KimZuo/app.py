import os
from flask import Flask, request, jsonify
from database import *
from upload.upload_plot import *

app = Flask(__name__)
# database_directory = os.path.join(os.getcwd(), "database", "farm_data.json")
test_database_directory = os.path.join(os.getcwd(), "database", "test_farm_data.json")
data = database_read(test_database_directory)


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
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_area = request.args.get('new_plot_area')

    # Call the function to update or add plot area
    success = update_or_add_plotArea(data, int(farm_id), int(building_id), int(plot_id), plot_date, int(new_plot_area))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding plot fruitlets
@app.route('/args/update_or_add_plot_fruitlets', methods=['POST'])
def update_or_add_fruitlets():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_fruitlets = request.args.get('new_plot_fruitlets')

    # Call the function to update or add plot fruitlets
    success = update_or_add_plotFruitlets(data, int(farm_id), int(building_id), int(plot_id), plot_date, int(new_plot_fruitlets))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Similarly, create routes for updating or adding plot volume and width

if __name__ == '__main__':
    app.run(debug=True)
