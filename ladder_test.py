import cv2
import numpy as np

image = cv2.imread("lad.png")
out = np.zeros((336,120,3), np.uint8)
rungs = np.zeros((336,120,3), np.uint8)

in_section = False
section_length = 0

for y in range(0, 336):
    print("Row: " + str(y))
    for x in range(0, 120):
        pix = image[y,x]
        if np.any(pix == (255,255,255)):
            section_length += 1
            in_section = True
        else:
            if in_section == True:
                in_section = False
                print("Section lenght:" + str(section_length))
                out[y,x - int(section_length / 2)] = (255,255,255)
                section_length = 0

in_section = False
section_length = 0

for x in range(0, 120):
    for y in range(0, 336):
        pix = image[y,x]
        if np.any(pix == (255,255,255)):
            section_length += 1
            in_section = True
        else:
            if in_section == True:
                in_section = False
                print("Section lenght:" + str(section_length))
                out[y - int(section_length / 2),x] = (255,255,255)
                section_length = 0

cv2.imwrite("out.png", out)
cv2.imwrite("rungs.png", rungs)
