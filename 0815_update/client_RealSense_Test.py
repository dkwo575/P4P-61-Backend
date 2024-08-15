import requests
import os
import socketio
import threading
import time

CLIENT_FOLDER = 'client_realsense'
if not os.path.exists(CLIENT_FOLDER):
    os.makedirs(CLIENT_FOLDER)

CLIENT_DOWNLOAD_FOLDER = 'client_realsense_download'
if not os.path.exists(CLIENT_DOWNLOAD_FOLDER):
    os.makedirs(CLIENT_DOWNLOAD_FOLDER)

# Define a unique client ID
CLIENT_ID = 'realsense_client'

# Define the name for the client, so it will be easy for store files
CLIENT_NAME = 'camera_laptop'


def upload_file(url, filename):
    try:
        with open(filename, 'rb') as file:
            files = {'file': file}
            data = {'client_id': CLIENT_ID, 'client_name': CLIENT_NAME}  # Include client ID and client name in form data
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            # Parse the response JSON and print it in a formatted manner
            response_data = response.json()
            print(
                f"Received response: File uploaded by client '{response_data['client_id']}':'{response_data['client_name']}' of type '{response_data['file_type']}': {response_data['message']}")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_file(url, filename, file_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(os.path.join(CLIENT_DOWNLOAD_FOLDER, filename), 'wb') as f:
            f.write(response.content)
        print(f"File '{filename}' downloaded successfully to '{CLIENT_DOWNLOAD_FOLDER}'")
        print(f"File type: {file_type}")
    except Exception as e:
        print(f"An error occurred: {e}")


def on_connect():
    print("Connected to server")


def on_disconnect():
    print("Disconnected from server")


def on_update(data):
    print(
        f"Received event: {data['event']} - {data['filename']} - Download URL: {data['download_url']} - Client ID: {data['client_id']} - Client Name: {data['client_name']}")

    # Check if the file was uploaded by the realsense client itself
    if data['client_name'] == CLIENT_NAME:
        print(f"Skipping file uploaded by the realsense client itself: {data['filename']}")
        return

    download_url = data['download_url']
    file_type = data.get('file_type', 'Unknown')  # Get file type or set to 'Unknown' if not provided
    download_file(download_url, data['filename'], file_type)
    time.sleep(0.1)  # Add a small delay


def subscribe_to_updates(url):
    sio = socketio.Client()
    sio.on('connect', on_connect)
    sio.on('disconnect', on_disconnect)
    sio.on('update', on_update)

    sio.connect(url)
    sio.wait()


if __name__ == '__main__':
    upload_url = 'http://127.0.0.1:5000/upload'
    subscribe_url = 'http://127.0.0.1:5000'  # WebSocket URL

    # Run the subscription in a separate thread
    subscription_thread = threading.Thread(target=subscribe_to_updates, args=(subscribe_url,))
    subscription_thread.start()

    # Test upload with client ID
    files_to_upload = [
        '20240530_114523_color.png',
        '20240530_114523_depthData.npy',
        '20240530_114527_color.png',
        '20240530_114527_depthData.npy',
        '20240530_123336_color.png',
        '20240530_123336_depthData.npy',
        '20240530_123339_color.png',
        '20240530_123339_depthData.npy',
        '20240530_123339_color.png',
        '20240530_123339_depthData.npy',
        '20240530_123346_color.png',
        '20240530_123346_depthData.npy',
        '20240530_124122_color.png',
        '20240530_124122_depthData.npy',
        '20240530_124127_color.png',
        '20240530_124127_depthData.npy',
        '20240530_124134_color.png',
        '20240530_124134_depthData.npy'
    ]

    for file_name in files_to_upload:
        upload_file(upload_url, os.path.join(CLIENT_FOLDER, file_name))
