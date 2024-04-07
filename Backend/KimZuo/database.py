import json


def database_read(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def database_write(file_path, data_write):
    with open(file_path, 'w') as file:
        json.dump(data_write, file)


# def newdata_join(data_key, data_value):
#     database_data = database_read(database_directory)
#     print(database_data)
#     database_data[data_key] = data_value
#     print(database_data)
#     database_write(database_directory, database_data)
