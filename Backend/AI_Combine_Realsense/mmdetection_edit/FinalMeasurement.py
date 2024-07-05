# FinalMeasurement.py

from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time
import random
import pyrealsense2 as rs
from scipy.ndimage import convolve
from numpy import median
import math
from PIL import Image, ImageFilter


def initialize_model(config_file, checkpoint_file):
    """
    Initialize the object detection model.
    """
    return init_detector(config_file, checkpoint_file, device='cpu')


def load_image(image_path):
    """
    Load an image using mmcv.
    """
    return mmcv.imread(image_path)


def load_depth_data(depth_path):
    """
    Load depth data from a .npy file.
    """
    return np.load(depth_path)


def perform_inference(model, img):
    """
    Perform inference using the model and image.
    """
    return inference_detector(model, img)


def visualize_results(model, img, result):
    """
    Visualize the inference results.
    """
    show_result_pyplot(model, img, result)


def extract_bboxes_and_segments(result):
    """
    Extract bounding boxes and segmentation results.
    """
    bbox_result, segm_result = result
    labels = [np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(bbox_result)]
    labels = np.concatenate(labels)
    bboxes = np.vstack(bbox_result)
    segm_result = [x for x in segm_result if x != []]
    segment = np.vstack(segm_result)
    return bboxes, segment


def draw_bboxes_on_image(image_path, output_path, bboxes, threshold=0.67, ):
    """
    Draw bounding boxes on the image.

    Args:
        image_path (str): Path to the input image.
        bboxes (list): List of bounding boxes. Each box is represented as [x1, y1, x2, y2, score].
        threshold (float): Score threshold to filter bounding boxes.

    Returns:
        np.ndarray: Image with bounding boxes drawn on it.
    """
    # Read the input image
    img = cv.imread(image_path, cv.IMREAD_COLOR)
    count = 0

    # Draw bounding boxes
    for bbox in bboxes:
        if bbox[4] > threshold:
            count += 1
            img = cv.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
            cv.putText(img, str(count),
                       (int((int(bbox[0]) + int(bbox[2])) / 2), int((int(bbox[1]) + int(bbox[3])) / 2)),
                       fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=3, thickness=3, color=(250, 225, 0))

    # Save the output image
    cv.imwrite(output_path, img)

    # Show the image (optional)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.show()

    # Return the modified image
    return img


def get_color_intrinsics():
    """
    Get color intrinsics for RealSense.
    """
    color_intrin = rs.pyrealsense2.intrinsics()
    color_intrin.width = 1280
    color_intrin.height = 720
    color_intrin.ppx = 646.9525146484375
    color_intrin.ppy = 375.3297119140625
    color_intrin.fx = 911.9494018554688
    color_intrin.fy = 912.0560302734375
    color_intrin.model = rs.pyrealsense2.distortion.inverse_brown_conrady
    color_intrin.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]
    return color_intrin


def find_circle(x1, y1, x2, y2, x3, y3):
    """
    Find the circle on which the given three points lie.
    """
    x12 = x1 - x2
    x13 = x1 - x3
    y12 = y1 - y2
    y13 = y1 - y3
    y31 = y3 - y1
    y21 = y2 - y1
    x31 = x3 - x1
    x21 = x2 - x1

    sx13 = pow(x1, 2) - pow(x3, 2)
    sy13 = pow(y1, 2) - pow(y3, 2)
    sx21 = pow(x2, 2) - pow(x1, 2)
    sy21 = pow(y2, 2) - pow(y1, 2)

    f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
                              ((y31) * (x12) - (y21) * (x13))))

    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
         (2 * ((x31) * (y12) - (x21) * (y13))))

    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1)

    h = -g
    k = -f
    sqr_of_r = h * h + k * k - c

    r = round(math.sqrt(sqr_of_r), 5)

    return r, [h, k]


def calculate_size(bboxes, segment, depth_data, color_intrin):
    """
    Calculate the tomato size using bounding boxes, segmentation, and depth data.
    """
    height_list = []
    width_list = []
    fill_percentage_list = []
    count = 0

    for bbox in bboxes:
        if bbox[4] > 0.7:
            mask = np.asarray(segment[count], dtype="uint8")
            fil = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
            output = np.where(convolve(mask, fil, mode='constant') > 0)
            edge_depth = [depth_data[output[0][i]][output[1][i]] for i in range(len(output[0]))]
            center_depth = median(edge_depth)

            radius_list = []
            center_list = []
            for _ in range(10000):
                random_list = random.sample(range(0, len(output[0])), 3)
                try:
                    radius, center = find_circle(output[1][random_list[0]], output[0][random_list[0]],
                                                 output[1][random_list[1]], output[0][random_list[1]],
                                                 output[1][random_list[2]], output[0][random_list[2]])
                    radius_list.append(radius)
                    center_list.append(center)
                except ZeroDivisionError:
                    continue

            median_radius = int(median(radius_list) + 0.5)
            x_list = [center[0] for center in center_list]
            y_list = [center[1] for center in center_list]

            x_median = int(median(x_list) + 0.5)
            y_median = int(median(y_list) + 0.5)

            x_min, x_max = int(bbox[0]), int(bbox[2])
            y_min, y_max = int(bbox[1]), int(bbox[3])
            x_mid = int((x_min + x_max) / 2)
            y_mid = int((y_min + y_max) / 2)

            top = [x_mid, y_min]
            bot = [x_mid, y_max]
            left = [x_min, y_mid]
            right = [x_max, y_mid]
            topC = rs.rs2_deproject_pixel_to_point(color_intrin, top, center_depth)
            botC = rs.rs2_deproject_pixel_to_point(color_intrin, bot, center_depth)
            leftC = rs.rs2_deproject_pixel_to_point(color_intrin, left, center_depth)
            rightC = rs.rs2_deproject_pixel_to_point(color_intrin, right, center_depth)

            new_height = math.sqrt(
                math.pow(topC[0] - botC[0], 2) + math.pow(topC[1] - botC[1], 2) + math.pow(topC[2] - botC[2], 2)) * 100
            new_width = math.sqrt(
                math.pow(leftC[0] - rightC[0], 2) + math.pow(leftC[1] - rightC[1], 2) + math.pow(leftC[2] - rightC[2],
                                                                                                 2)) * 100

            height_list.append(new_height * 100)
            width_list.append(new_width * 100)

            non_zero = np.transpose(np.nonzero(mask))
            mask_pixels_inside_circle = sum(
                1 for p in non_zero if ((y_median - p[0]) ** 2 + (x_median - p[1]) ** 2) <= median_radius ** 2
            )
            circle_area = int(math.pi * median_radius ** 2)
            fill_percentage = mask_pixels_inside_circle / circle_area
            fill_percentage_list.append(fill_percentage)

        count += 1

    return height_list, width_list, fill_percentage_list


def main_old(config_file, checkpoint_file, image_path, depth_path, output_path):
    """
    Main function to process the image and depth data.
    """
    img = load_image(image_path)
    model = initialize_model(config_file, checkpoint_file)
    # depth_data = load_depth_data(depth_path)
    result = perform_inference(model, img)
    # visualize_results(model, img, result)
    model.show_result(img, result, out_file=output_path)
    # bboxes, segment = extract_bboxes_and_segments(result)
    # color_intrin = get_color_intrinsics()
    # height_list, width_list, fill_percentage_list = calculate_size(bboxes, segment, depth_data, color_intrin)
    # draw_bboxes_on_image(image_path, bboxes, output_path)

    # return height_list, width_list, fill_percentage_list


def main(config_file, checkpoint_file, image_path, depth_path, output_path):
    """
    Main function to process the image and depth data.
    """
    img = load_image(image_path)
    model = initialize_model(config_file, checkpoint_file)
    result = perform_inference(model, img)
    model.show_result(img, result, out_file=output_path)


if __name__ == '__main__':
    config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
    checkpoint_file = 'laboro_tomato_little_48ep.pth'
    image_path = 'E:/Code/Python_WorkSPace/AI/mmdetection/client_download_ai/1_color.png'
    depth_path = 'E:/Code/Python_WorkSPace/AI/mmdetection/client_download_ai/1_depthData.npy'
    output_path = 'E:/Code/Python_WorkSPace/AI/mmdetection/client_ai/1_output.png'
    main(config_file, checkpoint_file, image_path, depth_path, output_path)

    # height_list, width_list, fill_percentage_list = main(config_file, checkpoint_file, image_path, depth_path, output_path)
    # print("Heights:", height_list)
    # print("Widths:", width_list)
    # print("Fill Percentages:", fill_percentage_list)
