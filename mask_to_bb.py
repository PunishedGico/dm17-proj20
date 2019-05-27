import cv2
import numpy as np

pad = 0
ignore = (0, 0, 0)

def mask_to_bb(mask):
    image = mask.copy()

    for x in range(1, np.size(mask, 1) - 1):
        for y in range(1, np.size(mask, 0) - 1):
            if (mask[y, x] != ignore).any():
                rect = cv2.floodFill(mask, None, (x, y), ignore)
                cv2.rectangle(image, (rect[-1][0], rect[-1][1]), (rect[-1][0]+rect[-1][2], rect[-1][1]+rect[-1][3]), (0,0,255), 2)

    #cv2.imwrite("out.png", image)
    cv2.imshow("bounding boxes", image)
    cv2.waitKey(0)

np_mask_to_bb(cv2.imread("mask.png"))