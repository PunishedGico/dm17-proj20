import cv2
import numpy as np

import data_converter

pad = 3
freq = 5
ignore = (0, 0, 0)

def mask_to_bb(mask):
    image = mask.copy()

    width = np.size(mask, 1)
    height = np.size(mask, 0)

    output_dict = {"detection_boxes": [], "detection_classes": [], "detection_scores": []}

    for x in range(1, width - 1, freq):
        for y in range(1, height - 1, freq):
            colour = mask[y, x].copy()
            if (colour != ignore).any():
                rect = cv2.floodFill(mask, None, (x, y), ignore)

                px = rect[-1][0]
                py = rect[-1][1]
                ox = rect[-1][2]
                oy = rect[-1][3]

                output_dict["detection_boxes"].append([py/height, px/width, (py+oy)/height, (px+ox)/width])
                output_dict["detection_classes"].append(int(colour[0]))
                output_dict["detection_scores"].append(1.0)

    return output_dict
