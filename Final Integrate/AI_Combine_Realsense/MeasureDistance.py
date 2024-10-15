import os
import numpy as np
import cv2
from glob import glob
from skimage.measure import label, regionprops, find_contours
import pyrealsense2 as rs
import math

""" Creating a directory """
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

""" Convert a mask to border image """
def mask_to_border(mask):
    h, w = mask.shape
    border = np.zeros((h, w))

    contours = find_contours(mask, 128)
    for contour in contours:
        for c in contour:
            x = int(c[0])
            y = int(c[1])
            border[x][y] = 255

    return border

""" Mask to bounding boxes """
def mask_to_bbox(mask):
    bboxes = []

    mask = mask_to_border(mask)
    lbl = label(mask)
    props = regionprops(lbl)
    for prop in props:
        x1 = prop.bbox[1]
        y1 = prop.bbox[0]

        x2 = prop.bbox[3]
        y2 = prop.bbox[2]

        bboxes.append([x1, y1, x2, y2])

    return bboxes

def parse_mask(mask):
    mask = np.expand_dims(mask, axis=-1)
    mask = np.concatenate([mask, mask, mask], axis=-1)
    return mask

if __name__ == "__main__":
    count = 0
    size = 0

    color_intrin = rs.pyrealsense2.intrinsics() #create a color intrinsics property
    color_intrin.width = 1280
    color_intrin.height = 720
    color_intrin.ppx = 646.9525146484375
    color_intrin.ppy = 375.3297119140625
    color_intrin.fx = 911.9494018554688
    color_intrin.fy = 912.0560302734375
    color_intrin.model = rs.pyrealsense2.distortion.inverse_brown_conrady
    color_intrin.coeffs = [0.0, 0.0, 0.0, 0.0, 0.0]

    """ Load the dataset """
    name = "8e72258622144c2d9bedc8e72c7f44b9"
    #name = "18f603892b0c4fafa58767a7e54f917e"
    #name = "74c5ef072ab14dcf99c2414f2f011627"
    #name = "76b589bdf6ae408e874c6c7f1c107249"
    #name = "1284d6dc2cac48cd9ffbc1ec694ffd1d"
    #name = "a806190ab7274b1a8aaedf03b313f073"
    #name = "aef4ff49c7b8472d83ac2394c9591608"
    #name = "c7a8abfa5db7472c9eecfb8074e94b13"
    #name = "fecc62e5098940daa6d72020883ffc8d"
    depthImage = np.load(f'C:/Users/skwe9/Desktop/images/{name} depthData.npy')
    x = cv2.imread(f"C:/Users/skwe9/Desktop/images/{name} color.png", cv2.IMREAD_COLOR)

    """ Detecting bounding boxes """
    bboxes = [[600, 344, 838, 593], [425, 334, 614, 534]]
    #bboxes = [[538, 409, 681, 545], [603, 278, 755, 436], [792, 508, 879, 600], [428, 379, 544, 514], [477, 256, 615, 400], [823, 439, 911, 527]]
    #bboxes = [[384, 450, 562, 634], [562, 430, 742, 621], [435, 236, 625, 429], [620, 249, 800, 428]]
    #bboxes = [[447, 240, 626, 419], [458, 421, 655, 612], [630, 312, 819, 487], [627, 483, 825, 685]]
    #bboxes = [[589, 323, 750, 486], [672, 444, 843, 609], [635, 171, 815, 342], [760, 277, 945, 472], [381, 540, 488, 653], [461, 493, 555, 584]]
    #bboxes = [[558, 415, 684, 536], [512, 292, 641, 419], [638, 320, 764, 454], [594, 187, 730, 329]]
    #bboxes = [[558, 216, 801, 452]]
    #bboxes = [[493, 227, 647, 387], [529, 377, 673, 519], [643, 272, 796, 435], [657, 434, 803, 569]]
    #bboxes = [[280, 160, 544, 408], [577, 69, 819, 309], [600, 287, 842, 547], [337, 378, 620, 688]]

    """ marking bounding box on image """
    for bbox in bboxes:
        x1 = bbox[0]
        x2 = bbox[2]
        xMid = int((bbox[0] + bbox[2])/2)
        yValue = int((bbox[3] + bbox[1])/2)
        left_point = depthImage[yValue][x1] #left point
        right_point = depthImage[yValue][x2] #right point
        center_point = depthImage[yValue][xMid]
        median_point = np.median(depthImage[int(bboxes[0][1]):int(bboxes[0][3]), int(bboxes[0][0]):int(bboxes[0][2])])
        print(str(left_point) + ',' + str(right_point))
        print(median_point)
        point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [x1, yValue], center_point)
        point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x2, yValue], center_point)

        # if(abs(left_point - right_point) > 0.15):
        #     chosen_point = min(left_point, right_point)
        #     point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [x1, yValue], chosen_point)
        #     point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x2, yValue], chosen_point)
        # else:
        #     point1 = rs.rs2_deproject_pixel_to_point(color_intrin, [x1, yValue], left_point)
        #     point2 = rs.rs2_deproject_pixel_to_point(color_intrin, [x2, yValue], right_point)

        dist = math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1],2) + math.pow(point1[2] - point2[2], 2))
        dist = 100*dist
        dist = "%.2f" % dist
        count = count + 1
        x = cv2.rectangle(x, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
        cv2.putText(x, f"tomato {count} = {dist}cm",(bbox[0], bbox[1]), fontFace = cv2.FONT_HERSHEY_PLAIN, fontScale = 1, color = (250,225,100))
        print(f"tomato {count} = {dist}cm")

    """ Saving the image """
    # cat_image = np.concatenate([x, parse_mask(y)], axis=1)
    cv2.imwrite(f"C:/Users/skwe9/Desktop/output/{name}_output.png", x)