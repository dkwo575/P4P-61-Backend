import os
from flask import Flask, request, jsonify
from database import *
from get.get_building import *
from get.get_environment import *
from get.get_event import *
from get.get_farm import *
from get.get_plot import *
from upload.upload_farm import *
from upload.upload_building import *
from upload.upload_event import *
from upload.upload_environment import *
from upload.upload_data import *
from upload.upload_plot import *

app = Flask(__name__)
# database_directory = os.path.join(os.getcwd(), "database", "farm_data.json")
test_database_directory = os.path.join(os.getcwd(), "database", "test_farm_data.json")
data = database_read(test_database_directory)


#
# upload_farm.py relate
#
@app.route('/args/update_or_add_farm_name', methods=['POST'])
def update_or_add_farm_name():
    farm_id = request.args.get('farm_id')
    new_farm_name = request.args.get('new_farm_name')

    # Call the function to update or add farm name
    success = update_or_add_farmName(data, int(farm_id), new_farm_name)
    print(success)
    return jsonify({'success': success})


#
# upload_building.py relate
#
@app.route('/args/update_or_add_building_name', methods=['POST'])
def update_or_add_building_name():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    new_building_name = request.args.get('new_building_name')

    # Call the function to update or add building name
    success = update_or_add_buildingName(data, int(farm_id), int(building_id), new_building_name)
    return jsonify({'success': success})


#
# upload_event.py relate
#
@app.route('/args/update_or_add_event', methods=['POST'])
def update_or_add_event_text():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    event_date = request.args.get('event_date')
    new_text = request.args.get('new_text')

    # Call the function to update or add plot name
    success = update_or_add_eventText(data, int(farm_id), int(building_id), event_date, new_text)
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


#
# upload_environment.py relate
#
# Route for updating or adding environment temperature
@app.route('/args/update_or_add_environment_temperature', methods=['POST'])
def update_or_add_environment_temperature():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')
    new_environment_temperature = request.args.get('new_environment_temperature')

    # Call the function to update or add plot name
    success = update_or_add_Temperature(data, int(farm_id), int(building_id), environment_date,
                                        int(new_environment_temperature))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding environment fluorescent
@app.route('/args/update_or_add_environment_fluorescent', methods=['POST'])
def update_or_add_environment_fluorescent():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')
    new_environment_fluorescent = request.args.get('new_environment_fluorescent')

    # Call the function to update or add plot name
    success = update_or_add_Fluorescents(data, int(farm_id), int(building_id), environment_date,
                                         int(new_environment_fluorescent))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding environment Co2 Concentration
@app.route('/args/update_or_add_environment_Co2Concentration', methods=['POST'])
def update_or_add_environment_Co2Concentration():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')
    new_environment_Co2Concentration = request.args.get('new_environment_Co2Concentration')

    # Call the function to update or add plot name
    success = update_or_add_Co2Concentration(data, int(farm_id), int(building_id), environment_date,
                                             int(new_environment_Co2Concentration))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding environment irrigation
@app.route('/args/update_or_add_environment_irrigation', methods=['POST'])
def update_or_add_environment_irrigation():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')
    new_environment_irrigation = request.args.get('new_environment_irrigation')

    # Call the function to update or add plot name
    success = update_or_add_Irrigation(data, int(farm_id), int(building_id), environment_date,
                                       int(new_environment_irrigation))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


#
# upload_data.py relate
#
# Route for updating or adding data area
@app.route('/args/update_or_add_data_area', methods=['POST'])
def update_or_add_data_area():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_area = request.args.get('new_data_area')

    # Call the function to update or add plot name
    success = update_or_add_Area(data, int(farm_id), int(building_id), data_date,
                                 int(new_data_area))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding data fruitlets
@app.route('/args/update_or_add_data_fruitlets', methods=['POST'])
def update_or_add_data_fruitlets():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_fruitlets = request.args.get('new_data_fruitlets')

    # Call the function to update or add plot name
    success = update_or_add_Fruitlets(data, int(farm_id), int(building_id), data_date,
                                      int(new_data_fruitlets))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding data height
@app.route('/args/update_or_add_data_height', methods=['POST'])
def update_or_add_data_height():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_height = request.args.get('new_data_height')

    # Call the function to update or add plot name
    success = update_or_add_Height(data, int(farm_id), int(building_id), data_date,
                                   int(new_data_height))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding data leaves
@app.route('/args/update_or_add_data_leaves', methods=['POST'])
def update_or_add_data_leaves():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_leaves = request.args.get('new_data_leaves')

    # Call the function to update or add plot name
    success = update_or_add_Leaves(data, int(farm_id), int(building_id), data_date,
                                   int(new_data_leaves))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding data volume
@app.route('/args/update_or_add_data_volume', methods=['POST'])
def update_or_add_data_volume():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_volume = request.args.get('new_data_volume')

    # Call the function to update or add plot name
    success = update_or_add_Volume(data, int(farm_id), int(building_id), data_date,
                                   int(new_data_volume))
    database_write(test_database_directory, success)
    print(success)
    return jsonify({'success': success})


# Route for updating or adding data volume
@app.route('/args/update_or_add_data_width', methods=['POST'])
def update_or_add_data_width():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    data_date = request.args.get('data_date')
    new_data_width = request.args.get('new_data_width')

    # Call the function to update or add plot name
    success = update_or_add_Width(data, int(farm_id), int(building_id), data_date,
                                  int(new_data_width))
    database_write(test_database_directory, success)
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
    new_plot_name = request.args.get('new_plot_name')

    # Call the function to update or add plot name
    success = update_or_add_plotName(data, int(farm_id), int(building_id), int(plot_id), new_plot_name)
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


# Route for updating or adding plot leaves
@app.route('/args/update_or_add_plot_leaves', methods=['POST'])
def update_or_add_plot_leaves():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')
    new_plot_leaves = request.args.get('new_plot_leaves')

    # Call the function to update or add plot volume
    success = update_or_add_plotLeaves(data, int(farm_id), int(building_id), int(plot_id), plot_date,
                                       int(new_plot_leaves))
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
@app.route('/args/update_or_add_plot_width', methods=['POST'])
def update_or_add_plot_width():
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


#
# get_farm.py relate
#
@app.route('/args/get_farm_name', methods=['GET'])
def get_farm_name():
    farm_id = request.args.get('farm_id')

    try:
        farm_name = get_farmName(data, int(farm_id))
        return jsonify({"farm_name": farm_name})
    except ValueError as e:
        return jsonify({"error": str(e)})


#
# get_building.py relate
#
@app.route('/args/get_building_name', methods=['GET'])
def get_building_name():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')

    try:
        building_name = get_buildingName(data, int(farm_id), int(building_id))
        return jsonify({"building_name": building_name})
    except ValueError as e:
        return jsonify({"error": str(e)})


#
# get_environment.py relate
#
@app.route('/args/get_environment_temperature', methods=['GET'])
def get_environment_temperature():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')

    try:
        temperature = get_Temperature(data, int(farm_id), int(building_id), environment_date)
        return jsonify({"temperature": temperature})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_environment_fluorescents', methods=['GET'])
def get_environment_fluorescents():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')

    try:
        fluorescents = get_Fluorescents(data, int(farm_id), int(building_id), environment_date)
        return jsonify({"fluorescent": fluorescents})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_environment_co2Concentration', methods=['GET'])
def get_environment_co2Concentration():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')

    try:
        co2Concentration = get_Co2Concentration(data, int(farm_id), int(building_id), environment_date)
        return jsonify({"Co2 Concentration": co2Concentration})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_environment_irrigation', methods=['GET'])
def get_environment_irrigation():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    environment_date = request.args.get('environment_date')

    try:
        irrigation = get_Irrigation(data, int(farm_id), int(building_id), environment_date)
        return jsonify({"irrigation": irrigation})
    except ValueError as e:
        return jsonify({"error": str(e)})


#
# get_event.py relate
#
@app.route('/args/get_event_text', methods=['GET'])
def get_event_text():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    event_date = request.args.get('event_date')

    try:
        event_text = get_eventText(data, int(farm_id), int(building_id), event_date)
        return jsonify({"event_text": event_text})
    except ValueError as e:
        return jsonify({"error": str(e)})


#
# get_plot.py relate
#
@app.route('/args/get_plot_name', methods=['GET'])
def get_plot_name():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')

    try:
        plot_name = get_plotName(data, int(farm_id), int(building_id), int(plot_id))
        return jsonify({"event_text": plot_name})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_area', methods=['GET'])
def get_plot_area():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_area = get_plotArea(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_area})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_fruitlets', methods=['GET'])
def get_plot_fruitlets():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_fruitlets = get_plotFruitlets(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_fruitlets})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_height', methods=['GET'])
def get_plot_height():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_height = get_plotHeight(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_height})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_leaves', methods=['GET'])
def get_plot_leaves():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_leaves = get_plotLeaves(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_leaves})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_volume', methods=['GET'])
def get_plot_volume():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_volume = get_plotVolume(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_volume})
    except ValueError as e:
        return jsonify({"error": str(e)})


@app.route('/args/get_plot_width', methods=['GET'])
def get_plot_width():
    farm_id = request.args.get('farm_id')
    building_id = request.args.get('building_id')
    plot_id = request.args.get('plot_id')
    plot_date = request.args.get('plot_date')

    try:
        plot_width = get_plotWidth(data, int(farm_id), int(building_id), int(plot_id), plot_date)
        return jsonify({"event_text": plot_width})
    except ValueError as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
