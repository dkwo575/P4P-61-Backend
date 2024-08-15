import requests
import os
import socketio
import threading
from time import sleep
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import uuid
from datetime import datetime

CLIENT_FOLDER = 'client_realsense'
if not os.path.exists(CLIENT_FOLDER):
    os.makedirs(CLIENT_FOLDER)

CLIENT_DOWNLOAD_FOLDER = 'client_realsense_download'
if not os.path.exists(CLIENT_DOWNLOAD_FOLDER):
    os.makedirs(CLIENT_DOWNLOAD_FOLDER)

# Define a unique client ID
CLIENT_ID = 'realsense_client'


# Client Communication

def upload_file(url, filename):
    try:
        with open(filename, 'rb') as file:
            files = {'file': file}
            data = {'client_id': CLIENT_ID}  # Include client ID in form data
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            # Parse the response JSON and print it in a formatted manner
            response_data = response.json()
            print(
                f"Received response: File uploaded by client '{response_data['client_id']}' of type '{response_data['file_type']}': {response_data['message']}")
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
        f"Received event: {data['event']} - {data['filename']} - Download URL: {data['download_url']} - Client ID: {data['client_id']}")

    # Check if the file was uploaded by the realsense client itself
    if data['client_id'] == CLIENT_ID:
        print(f"Skipping file uploaded by the realsense client itself: {data['filename']}")
        return

    download_url = data['download_url']
    file_type = data.get('file_type', 'Unknown')  # Get file type or set to 'Unknown' if not provided
    download_file(download_url, data['filename'], file_type)
    sleep(0.1)  # Add a small delay


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

    try:
        sio.connect(url)
        sio.wait()
    except socketio.exceptions.ConnectionError as e:
        print(f"Connection failed: {e}")
        sleep(5)  # Wait for 5 seconds before attempting to reconnect
        subscribe_to_updates(url)  # Recursive call to retry connection


# Realsense Take Picture

def findDevices():
    ctx = rs.context()  # Create librealsense context for managing devices
    serials = []
    if len(ctx.devices) > 0:
        for dev in ctx.devices:
            print('Found device: ', \
                  dev.get_info(rs.camera_info.name), ' ', \
                  dev.get_info(rs.camera_info.serial_number))
            serials.append(dev.get_info(rs.camera_info.serial_number))
    else:
        print("No Intel Device connected")

    return serials, ctx


def enableDevices(serials, ctx, resolution_width, resolution_height, frame_rate):
    pipelines = []
    for serial in serials:
        pipe = rs.pipeline(ctx)
        cfg = rs.config()
        cfg.enable_device(serial)
        cfg.enable_stream(rs.stream.depth, resolution_width, resolution_height, rs.format.z16, frame_rate)
        cfg.enable_stream(rs.stream.color, resolution_width, resolution_height, rs.format.bgr8, frame_rate)
        pipe.start(cfg)
        pipelines.append([serial, pipe])

    return pipelines


def Visualize(pipelines, upload_url):
    align_to = rs.stream.color
    align = rs.align(align_to)

    for (device, pipe) in pipelines:
        # Get frameset of color and depth
        frames = pipe.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image
        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        # print(aligned_depth_frame.get_distance(100,100))
        color_frame = aligned_frames.get_color_frame()
        color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
        # print(color_intrinsics.width)
        # print(color_intrinsics.height)
        # print(color_intrinsics.ppx)
        # print(color_intrinsics.ppy)
        # print(color_intrinsics.fx)
        # print(color_intrinsics.fy)
        # print(color_intrinsics.model)
        # print(color_intrinsics.coeffs)

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(aligned_depth_frame)

        hole_filling = rs.hole_filling_filter(2)
        filled_depth = hole_filling.process(filtered_depth)
        filled_depth = filled_depth.as_depth_frame()  # https://github.com/IntelRealSense/librealsense/issues/2521

        depth_image = np.asanyarray(filled_depth.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Render images
        depth_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_image, alpha=0.03), cv.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))

        cv.imshow('RealSense' + device, images)
        key = cv.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv.destroyAllWindows()
            return True

        # create a new empty depth array which we will save our distance values
        depth_array = np.empty((color_intrinsics.height, color_intrinsics.width), dtype=np.float64)

        # Save images and depth maps from both cameras by pressing 's'
        if key == 115:
            for h in range(color_intrinsics.height):
                for w in range(color_intrinsics.width):
                    depth_array[h][w] = filled_depth.get_distance(w, h)
            unique_filename = str(uuid.uuid4().hex)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            npy_name = os.path.join(CLIENT_FOLDER, f'{timestamp}_depthData.npy')
            png_name = os.path.join(CLIENT_FOLDER, f'{timestamp}_color.png')
            np.save(npy_name, depth_array)
            cv.imwrite(png_name, color_image)
            print(filled_depth.get_distance(100, 100))
            upload_file(upload_url, png_name)
            upload_file(upload_url, npy_name)


def pipelineStop(pipelines):
    for (device, pipe) in pipelines:
        # Stop streaming
        pipe.stop()


if __name__ == '__main__':
    upload_url = 'http://130.216.238.175:5000/upload'
    subscribe_url = 'http://130.216.238.175:5000'  # WebSocket URL

    # Run the subscription in a separate thread
    subscription_thread = threading.Thread(target=subscribe_to_updates, args=(subscribe_url,))
    subscription_thread.start()

    # Combine Realsense Take Image Code:
    serials, ctx = findDevices()

    # Define some constants (resolution in pixels)
    resolution_width = 1280  # 640
    resolution_height = 720  # 480
    frame_rate = 15  # fps
    count = 0

    pipelines = enableDevices(serials, ctx, resolution_width, resolution_height, frame_rate)

    try:
        while True:
            exit_program = Visualize(pipelines, upload_url)
            if exit_program:
                print('Program closing...')
                break

    finally:
        pipelineStop(pipelines)
