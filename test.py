import cv2 as cv
import numpy as np
from helper import *

frame = cv.imread("/Users/stevengong/Projects/HackMIT/image.jpg")
median_grayscale = np.median(frame)
im_gray = get_grayscale(frame)
(thresh, im_bw) = cv2.threshold(im_gray, 100, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

"""alternative if you know the threshold
thresh = 127
im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
"""
thresh = 160
im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
# im_bw = cv.adaptiveThreshold(im_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv.THRESH_BINARY,11,2)
cv.imwrite("./result.png", im_bw)
