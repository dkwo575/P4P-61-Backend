import requests
import os
import socketio
import threading
import time
import FinalMeasurement

# Directories for file operations
CLIENT_DOWNLOAD_FOLDER = 'client_download_ai'
if not os.path.exists(CLIENT_DOWNLOAD_FOLDER):
    os.makedirs(CLIENT_DOWNLOAD_FOLDER)

CLIENT_UPLOAD_FOLDER = 'client_ai'
if not os.path.exists(CLIENT_UPLOAD_FOLDER):
    os.makedirs(CLIENT_UPLOAD_FOLDER)

# Define a unique client ID
CLIENT_ID = 'ai_client'

# Define the name for the client, so it will be easy for store files
CLIENT_NAME = 'ai_mmdetection'

# Avoid reprocessing files based on their names
PROCESSED_MARKER = '_processed'

# Track pending downloads
pending_images = set()
pending_depths = set()

# Create a lock for processing files
processing_lock = threading.Lock()


def upload_file(url, filename):
    try:
        with open(filename, 'rb') as file:
            files = {'file': file}
            data = {'client_id': CLIENT_ID,
                    'client_name': CLIENT_NAME}  # Include client ID and client name in form data
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

        # Add to pending downloads and attempt to process
        if file_type == 'PNG':
            pending_images.add(filename)
            attempt_processing(filename.replace('color.png', 'depthData.npy'))
        elif file_type == 'NPY':
            pending_depths.add(filename)
            attempt_processing(filename.replace('depthData.npy', 'color.png'))

    except Exception as e:
        print(f"An error occurred during file download: {e}")


def attempt_processing(filename):
    """Try to process files if both .png and .npy are available."""
    image_file = filename.replace('depthData.npy', 'color.png')
    depth_file = filename.replace('color.png', 'depthData.npy')

    if image_file in pending_images and depth_file in pending_depths:
        print(f"Attempting to process image '{image_file}' with depth data '{depth_file}'")

        # Start a thread to process files
        threading.Thread(target=process_files, args=(image_file, depth_file)).start()
    else:
        print(f"Waiting for corresponding files: {image_file} or {depth_file}")


def on_connect():
    print("Connected to server")


def on_disconnect():
    print("Disconnected from server")


def on_update(data):
    print(
        f"Received event: {data['event']} - {data['filename']} - Download URL: {data['download_url']} - Client ID: {data['client_id']}")

    # Check if the file was uploaded by the AI client itself
    if data['client_id'] == CLIENT_ID:
        print(f"Skipping file uploaded by the AI client itself: {data['filename']}")
        return

    download_url = data['download_url']
    filename = data['filename']
    file_type = data.get('file_type', 'Unknown')  # Get file type or set to 'Unknown' if not provided

    if PROCESSED_MARKER in filename:
        print(f"Skipping already processed file: {filename}")
        return

    download_file(download_url, filename, file_type)


def on_send_file_to_ai(data):
    print(f"Received files for processing: {data['image_download_url']} and {data['depth_download_url']}")

    image_download_url = data['image_download_url']
    depth_download_url = data['depth_download_url']

    download_file(image_download_url, data['image_file'], 'PNG')
    download_file(depth_download_url, data['depth_file'], 'NPY')


def subscribe_to_updates(url):
    sio = socketio.Client(
        reconnection=True,
        reconnection_attempts=5,
        reconnection_delay=1,
        reconnection_delay_max=5
    )
    sio.on('connect', on_connect)
    sio.on('disconnect', on_disconnect)
    sio.on('update', on_update)
    sio.on('send_file_to_ai', on_send_file_to_ai)  # Register the new event listener

    try:
        sio.connect(url)
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print(f"Connection failed: {e}")
        time.sleep(5)  # Wait for 5 seconds before attempting to reconnect
        subscribe_to_updates(url)  # Recursive call to retry connection


def process_files(image_filename, depth_filename):
    with processing_lock:
        print(f"Processing files: {image_filename} and {depth_filename}")
        try:
            image_path = os.path.join(CLIENT_DOWNLOAD_FOLDER, image_filename)
            depth_path = os.path.join(CLIENT_DOWNLOAD_FOLDER, depth_filename)
            output_path = os.path.join(CLIENT_UPLOAD_FOLDER,
                                       os.path.basename(image_filename).replace('.png', f'{PROCESSED_MARKER}.png'))

            # AI processing using mmdetection
            FinalMeasurement.main(config_file, checkpoint_file, image_path, depth_path, output_path)

            print(f"Processed file saved to '{output_path}'")

            # Upload the processed file
            upload_file(upload_url, output_path)
        except Exception as e:
            print(f"An error occurred during processing: {e}")


if __name__ == '__main__':
    subscribe_url = 'http://127.0.0.1:5000'  # WebSocket URL
    upload_url = 'http://127.0.0.1:5000/upload'
    config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
    checkpoint_file = 'laboro_tomato_big_48ep.pth'

    # Run the subscription in a separate thread
    subscription_thread = threading.Thread(target=subscribe_to_updates, args=(subscribe_url,))
    subscription_thread.start()

    # Keep the main thread alive to allow the socket to remain connected
    while True:
        time.sleep(1)
