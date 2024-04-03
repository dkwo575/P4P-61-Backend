import json
import os

current_directory = os.getcwd()
database_directory = os.getcwd() + "\database"


def database_read(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def database_write(file_path, data_write):
    with open(file_path, 'w') as file:
        json.dump(data_write, file)


if __name__ == '__main__':
    write_file_path = database_directory + "\\test.txt"
    data_in = {"date": '2023-06-11', "temperature": '23.4', "fluorescent": '6993',
               "co2Concentration": '781', "irrigation": '2.0'}
    print(write_file_path)
    database_write(write_file_path, data_in)
