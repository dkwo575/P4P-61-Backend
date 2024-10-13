#%%
from mmdet.apis import init_detector, inference_detector, show_result_pyplot
import mmcv
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time
import random

config_file = 'configs/mask_rcnn/mask_rcnn_r50_fpn_1x_coco.py'
# download the checkpoint from model zoo and put it in `checkpoints/`
# url: https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth
checkpoint_file = 'laboro_tomato_little_48ep.pth'
# checkpoint_file = 'epoch_42.pth'
#%%
imagePath = 'lightedImages/angle1/2.png'
depthPath = 'lightedImages/angle1/2.npy'

# build the model from a config file and a checkpoint file
img = mmcv.imread(imagePath)
model = init_detector(config_file, checkpoint_file, device='cpu')
depthData = np.load(depthPath)
result = inference_detector(model, img)
show_result_pyplot(model, img, result)

bbox_result, segm_result = result

labels = [
    np.full(bbox.shape[0], i, dtype=np.int32) \
    for i, bbox in enumerate(bbox_result)
]
labels = np.concatenate(labels)
bboxes = np.vstack(bbox_result)

segm_result = [x for x in segm_result if x != []]
segment = np.vstack(segm_result)

print(bboxes)
#%%
import cv2

x = cv2.imread(imagePath, cv2.IMREAD_COLOR)
count = 0
for bbox in bboxes:
    if bbox[4] > 0.67:
        count += 1
        x = cv2.rectangle(x, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (255, 0, 0), 2)
        cv2.putText(x, str(count), (int((int(bbox[0]) + int(bbox[2])) / 2), int((int(bbox[1]) + int(bbox[3])) / 2)),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=3, thickness=3, color=(250, 225, 0))

cv2.imwrite('lightedImages/angle2/order.png', x)
plt.imshow(x)
print(count)
#%%
import pyrealsense2 as rs

color_intrin = rs.pyrealsense2.intrinsics()  #create a color intrinsics property
color_intrin.width = 1280
color_intrin.height = 720
color_intrin.ppx = 646.9525146484375
color_intrin.ppy = 375.3297119140625
color_intrin.fx = 911.9494018554688
color_intrin.fy = 912.0560302734375
color_intrin.model = rs.pyrealsense2.distortion.inverse_brown_conrady
color_intrin.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]
#%%
from math import sqrt


# Function to find the circle on
# which the given three points lie
def findCircle(x1, y1, x2, y2, x3, y3):
    x12 = x1 - x2;
    x13 = x1 - x3;

    y12 = y1 - y2;
    y13 = y1 - y3;

    y31 = y3 - y1;
    y21 = y2 - y1;

    x31 = x3 - x1;
    x21 = x2 - x1;

    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2);

    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2);

    sx21 = pow(x2, 2) - pow(x1, 2);
    sy21 = pow(y2, 2) - pow(y1, 2);

    f = (((sx13) * (x12) + (sy13) *
          (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
                              ((y31) * (x12) - (y21) * (x13))));

    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
         (2 * ((x31) * (y12) - (x21) * (y13))));

    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1);

    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g;
    k = -f;
    sqr_of_r = h * h + k * k - c;

    # r is the radius
    r = round(sqrt(sqr_of_r), 5);

    # print("Centre = (", h, ", ", k, ")");
    # print("Radius = ", r);
    return r, [h, k]


#%%
import math
from scipy.ndimage import convolve
from PIL import Image, ImageFilter
from numpy import median


# THIS FUNCTION CALCULATES THE TOMATO SIZE USING THE BOUNDING BOXES, SEGMENTATION AND DEPTHDATA #
# RETURNS A LIST OF SIZES AND CORRESPONDING LIST OF fill percentage - higher THE percentage, THE MORE ACCURATE THE SIZE MEASUREMENT #

def calculateSize(bboxes, segment, depthData):
    heightList = []
    widthList = []
    fillPercentageList = []
    count = 0

    for bbox in bboxes:
        if bbox[4] > 0.7:
            ### FIND EDGE DEPTH ###
            mask = np.asarray(segment[count], dtype="uint8")  #get corresponding segmentation mask as binary matrix

            fil = [[-1, -1, -1],
                   [-1, 8, -1],
                   [-1, -1, -1]]

            output = np.where(convolve(mask, fil, mode='constant') > 0)

            edgeDepth = []

            for length in range(len(output[0])):
                edgeDepth.append(depthData[output[0][length]][output[1][length]])

            centerDepth = median(edgeDepth)

            ### CIRCLE FITTING ###
            radiusList = []
            centerList = []

            for i in range(10000):  #sample 3 random points and generate a circle
                randomList = random.sample(range(0, len(output[0])), 3)
                firstPoint = randomList[0]
                secondPoint = randomList[1]
                thirdPoint = randomList[2]
                try:
                    radius, center = findCircle(output[1][firstPoint], output[0][firstPoint], output[1][secondPoint],
                                                output[0][secondPoint], output[1][thirdPoint], output[0][thirdPoint])
                    radiusList.append(radius)
                    centerList.append(center)
                except ZeroDivisionError:
                    continue

            medianRadius = int(median(radiusList) + 0.5)

            xList = []
            yList = []

            for i in range(len(radiusList)):
                xList.append(centerList[i][0])
                yList.append(centerList[i][1])

            xMedian = int(median(xList) + 0.5)  #center coordinates
            yMedian = int(median(yList) + 0.5)  #center coordinates

            ### CALCULATE SIZE ###
            xMin = int(bbox[0])
            xMax = int(bbox[2])
            yMin = int(bbox[1])
            yMax = int(bbox[3])
            xMid = int((xMin + xMax) / 2)
            yMid = int((yMin + yMax) / 2)

            top = [xMid, yMin]
            bot = [xMid, yMax]
            left = [xMin, yMid]
            right = [xMax, yMid]
            topC = rs.rs2_deproject_pixel_to_point(color_intrin, top, centerDepth)
            botC = rs.rs2_deproject_pixel_to_point(color_intrin, bot, centerDepth)
            leftC = rs.rs2_deproject_pixel_to_point(color_intrin, left, centerDepth)
            rightC = rs.rs2_deproject_pixel_to_point(color_intrin, right, centerDepth)

            new_height = math.sqrt(
                math.pow(topC[0] - botC[0], 2) + math.pow(topC[1] - botC[1], 2) + math.pow(topC[2] - botC[2], 2)) * 100
            new_width = math.sqrt(
                math.pow(leftC[0] - rightC[0], 2) + math.pow(leftC[1] - rightC[1], 2) + math.pow(leftC[2] - rightC[2],
                                                                                                 2)) * 100

            heightList.append(new_height * 100)
            widthList.append(new_width * 100)

            ### calculate how much the segmentation mask fills up the drawn circle ###
            maskPixelsInsideCircle = 0
            totalMaskPixels = 0

            nonZero = np.transpose(np.nonzero(mask))

            for length in range(len(nonZero)):
                totalMaskPixels += 1
                if (((yMedian - nonZero[length][0]) ** 2 + (xMedian - nonZero[length][1]) ** 2) > medianRadius ** 2):
                    continue
                else:
                    maskPixelsInsideCircle += 1
            circleArea = int(math.pi * medianRadius ** 2)
            fillPercentage = maskPixelsInsideCircle / circleArea
            fillPercentageList.append(fillPercentage)

        count = count + 1

    return heightList, widthList, fillPercentageList


#%%
heightList, widthList, fillPercentageList = calculateSize(bboxes, segment, depthData)
print(heightList)
print(widthList)
print(fillPercentageList)
#%%
