# Libraries
import pyrealsense2 as rs
import numpy as np
import cv2 as cv
import os
import uuid
from datetime import *


def findDevices():
    ctx = rs.context()  # Create librealsense context for managing devices
    serials = []
    if (len(ctx.devices) > 0):
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


def Visualize(pipelines):
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
            npy_name = f'{timestamp} depthData.npy'
            png_name = f'{timestamp} color.png'
            np.save(f'{timestamp} depthData.npy', depth_array)
            cv.imwrite(f'{timestamp} color.png', color_image)
            print(filled_depth.get_distance(100, 100))
            print('Save')


def pipelineStop(pipelines):
    for (device, pipe) in pipelines:
        # Stop streaming
        pipe.stop()

    # -------Main program--------


if __name__ == '__main__':
    # directory = r'C:/Users/skwe9/Desktop/images'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_get_directory = os.path.join(current_directory, 'client_realsense')
    # directory = r'E:/Code/Python_WorkSPace/TakeImageRaw/DataGet'
    directory = data_get_directory
    os.chdir(directory)

    serials, ctx = findDevices()

    # Define some constants (resolution in pixels)
    resolution_width = 1280  # 640
    resolution_height = 720  # 480
    frame_rate = 15  # fps
    count = 0

    pipelines = enableDevices(serials, ctx, resolution_width, resolution_height, frame_rate)

    try:
        while True:
            exit = Visualize(pipelines)
            if exit == True:
                print('Program closing...')
                break
    finally:
        pipelineStop(pipelines)
