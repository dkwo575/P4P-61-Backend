# %% Importing necessary libraries
from mmdet.apis import init_detector, inference_detector
import mmcv
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import random
import os
import pyrealsense2 as rs
from scipy.ndimage import convolve

# This function calculates the size of tomatoes using the bounding boxes, segmentation, and depth data
def calculateSize(bboxes, segment, depthData, color_intrin):
    heightList = []
    widthList = []
    fillPercentageList = []

    for count, bbox in enumerate(bboxes):
        if bbox[4] > 0.7:  # Check if the confidence score is greater than 0.7
            ### FIND EDGE DEPTH ###
            mask = np.asarray(segment[count], dtype="uint8")  # Get segmentation mask as binary matrix

            fil = [[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]]

            output = np.where(convolve(mask, fil, mode='constant') > 0)
            edgeDepth = [depthData[output[0][i]][output[1][i]] for i in range(len(output[0]))]

            centerDepth = np.median(edgeDepth) if edgeDepth else 0

            ### CIRCLE FITTING ###
            radiusList = []
            centerList = []

            for _ in range(10000):  # Sample 3 random points and generate a circle
                if len(output[0]) < 3:  # Not enough points to sample
                    continue
                randomList = random.sample(range(len(output[0])), 3)
                firstPoint, secondPoint, thirdPoint = randomList

                radius, center = findCircle(
                    output[1][firstPoint], output[0][firstPoint],
                    output[1][secondPoint], output[0][secondPoint],
                    output[1][thirdPoint], output[0][thirdPoint]
                )
                if radius is not None:
                    radiusList.append(radius)
                    centerList.append(center)

            # Check if we found any valid radius values
            if radiusList:
                medianRadius = int(np.median(radiusList) + 0.5)
                xList = [center[0] for center in centerList]
                yList = [center[1] for center in centerList]

                xMedian = int(np.median(xList) + 0.5)  # Center coordinates
                yMedian = int(np.median(yList) + 0.5)  # Center coordinates

                ### CALCULATE SIZE ###
                xMin, xMax = int(bbox[0]), int(bbox[2])
                yMin, yMax = int(bbox[1]), int(bbox[3])
                xMid, yMid = (xMin + xMax) // 2, (yMin + yMax) // 2

                top = [xMid, yMin]
                bot = [xMid, yMax]
                left = [xMin, yMid]
                right = [xMax, yMid]

                topC = rs.rs2_deproject_pixel_to_point(color_intrin, top, centerDepth)
                botC = rs.rs2_deproject_pixel_to_point(color_intrin, bot, centerDepth)
                leftC = rs.rs2_deproject_pixel_to_point(color_intrin, left, centerDepth)
                rightC = rs.rs2_deproject_pixel_to_point(color_intrin, right, centerDepth)

                new_height = np.linalg.norm(np.array(topC) - np.array(botC)) * 100
                new_width = np.linalg.norm(np.array(leftC) - np.array(rightC)) * 100

                heightList.append(new_height)
                widthList.append(new_width)

                ### Calculate fill percentage ###
                maskPixelsInsideCircle = np.sum((yMedian - output[0]) ** 2 + (xMedian - output[1]) ** 2 <= medianRadius ** 2)
                circleArea = int(np.pi * medianRadius ** 2)
                fillPercentage = maskPixelsInsideCircle / circleArea if circleArea > 0 else 0  # Avoid division by zero
                fillPercentageList.append(fillPercentage)

    return heightList, widthList, fillPercentageList

# Find the circle on which the given three points lie
def findCircle(x1, y1, x2, y2, x3, y3):
    x12 = x1 - x2
    x13 = x1 - x3

    y12 = y1 - y2
    y13 = y1 - y3

    y31 = y3 - y1
    y21 = y2 - y1

    x31 = x3 - x1
    x21 = x2 - x1

    denom = (y31 * x12 - y21 * x13)
    if denom == 0:
        return None, [0, 0]  # Handle the case of collinearity

    sx13 = x1**2 - x3**2
    sy13 = y1**2 - y3**2
    sx21 = x2**2 - x1**2
    sy21 = y2**2 - y1**2

    f = ((sx13 * x12 + sy13 * x12 + sx21 * x13 + sy21 * x13) / (2 * denom))
    g = ((sx13 * y12 + sy13 * y12 + sx21 * y13 + sy21 * y13) / (2 * denom))

    c = (-x1**2 - y1**2 - 2 * g * x1 - 2 * f * y1)

    h = -g
    k = -f
    r = round(np.sqrt(h**2 + k**2 - c), 5)

    return r, [h, k]


# Modify the main function
def main(config_file, checkpoint_file, image_path, depth_path, output_path):
    # Read the image
    img = mmcv.imread(image_path)

    # Initialize the object detection model on CPU
    model = init_detector(config_file, checkpoint_file, device='cpu')

    # Load the depth data
    depth_data = np.load(depth_path)

    # Perform object detection inference
    result = inference_detector(model, img)

    # Unpack results
    bbox_result, segm_result = result
    labels = np.concatenate([np.full(bbox.shape[0], i, dtype=np.int32) for i, bbox in enumerate(bbox_result)])
    bboxes = np.vstack(bbox_result)
    segm_result = [x for x in segm_result if x != []]

    # Only proceed if there are segmentation results
    if segm_result:
        segment = np.vstack(segm_result)
    else:
        segment = np.array([])

    # Filter out bounding boxes based on confidence before calculating sizes
    filtered_bboxes = [bbox for bbox in bboxes if bbox[4] > 0.67]

    # Calculate the sizes
    color_intrin = rs.pyrealsense2.intrinsics()
    color_intrin.width = 1280
    color_intrin.height = 720
    color_intrin.ppx = 646.9525146484375
    color_intrin.ppy = 375.3297119140625
    color_intrin.fx = 911.9494018554688
    color_intrin.fy = 912.0560302734375
    color_intrin.model = rs.pyrealsense2.distortion.inverse_brown_conrady
    color_intrin.coeffs = [0.0] * 5

    height_list, width_list, fill_percentage_list = calculateSize(filtered_bboxes, segment, depth_data, color_intrin)

    # Show results
    for i, bbox in enumerate(filtered_bboxes):
        # Use the filtered list to get height, width, and fill percentage
        if i < len(height_list) and i < len(width_list) and i < len(fill_percentage_list):
            # Draw bounding box and sizes
            img = cv.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
            cv.putText(img, f"H: {height_list[i]:.2f}", (int(bbox[0]), int(bbox[1] - 10)), cv.FONT_HERSHEY_PLAIN, 1,
                       (250, 225, 0), 2)
            cv.putText(img, f"W: {width_list[i]:.2f}", (int(bbox[0]), int(bbox[1] - 30)), cv.FONT_HERSHEY_PLAIN, 1,
                       (250, 225, 0), 2)
            cv.putText(img, f"F: {fill_percentage_list[i]:.2f}", (int(bbox[0]), int(bbox[1] - 50)),
                       cv.FONT_HERSHEY_PLAIN, 1, (250, 225, 0), 2)
        else:
            print(f"Warning: Size lists are shorter than expected for bbox index {i}.")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the result image
    mmcv.imwrite(img, output_path)
    plt.imshow(img)
    plt.axis('off')  # Hide axes
    plt.show()


if __name__ == '__main__':
    config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
    checkpoint_file = 'laboro_tomato_big_48ep.pth'
    image_path = 'E:/Code/Python_WorkSPace/AI_Combine_Realsense/mmdetection/client_download_ai/20240530_114523_color.png'
    depth_path = 'E:/Code/Python_WorkSPace/AI_Combine_Realsense/mmdetection/client_download_ai/20240530_114523_depthData.npy'
    output_path = 'E:/Code/Python_WorkSPace/AI_Combine_Realsense/mmdetection/client_size_ai/20240530_114523_color_processed.png'
    main(config_file, checkpoint_file, image_path, depth_path, output_path)
