import os
from flask import Flask, request, jsonify
from database import *
from upload.upload_plot import *

app = Flask(__name__)
# database_directory = os.path.join(os.getcwd(), "database", "farm_data.json")
test_database_directory = os.path.join(os.getcwd(), "database", "test_farm_data.json")
data = database_read(test_database_directory)


#
# upload_farm.py relate
#
@app.route('/args/update_or_add_farm_name', methods=['POST'])
def update_or_add_farmName():
    farm_id = request.args.get('farm_id')
    new_farm_name = request.args.get('new_farm_name')

    # Call the function to update or add farm name
    success = update_or_add_farmName(data, int(farm_id), new_farm_name)
    print(success)
    return jsonify({'success': success})


#
# upload_plot.py relate
#

# Route for updating or adding plot name
@app.route('/args/update_or_add_plot_name', methods=['POST'])
def update_or_add_plot_name():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_name = request.args.get('new_plot_name')

    # Call the function to update or add plot name
    success = update_or_add_plotName(data, int(farm_id), int(building_id), int(plot_id), plot_date, new_plot_name)
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding plot area
@app.route('/args/update_or_add_plot_area', methods=['POST'])
def update_or_add_plot_area():
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
def update_or_add_plot_fruitlets():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_fruitlets = request.args.get('new_plot_fruitlets')

    # Call the function to update or add plot fruitlets
    success = update_or_add_plotFruitlets(data, int(farm_id), int(building_id), int(plot_id), plot_date,
                                          int(new_plot_fruitlets))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding plot height
@app.route('/args/update_or_add_plot_height', methods=['POST'])
def update_or_add_plot_height():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_height = request.args.get('new_plot_height')

    # Call the function to update or add plot height
    success = update_or_add_plotHeight(data, int(farm_id), int(building_id), int(plot_id), plot_date,
                                       int(new_plot_height))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding plot volume
@app.route('/args/update_or_add_plot_volume', methods=['POST'])
def update_or_add_plot_volume():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_volume = request.args.get('new_plot_volume')

    # Call the function to update or add plot volume
    success = update_or_add_plotVolume(data, int(farm_id), int(building_id), int(plot_id), plot_date,
                                       int(new_plot_volume))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding plot width
@app.route('/args/update_or_add_plot_volume', methods=['POST'])
def update_or_add_plot_volume():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_width = request.args.get('new_plot_width')

    # Call the function to update or add plot width
    success = update_or_add_plotWidth(data, int(farm_id), int(building_id), int(plot_id), plot_date,
                                      int(new_plot_width))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Similarly, create routes for updating or adding plot volume and width

if __name__ == '__main__':
    app.run(debug=True)
