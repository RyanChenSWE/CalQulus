# Import required packages
import cv2
import numpy as np
def get_bbox(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  ret, img_thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
  #img_thresh1 = cv2.adaptiveThreshold(gray.astype(np.uint8),255,1,1,11,2)
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))
  img_dilated = cv2.dilate(img_thresh1, rect_kernel, iterations = 1)
  contours, hierarchy = cv2.findContours(img_dilated, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)
  cv2.imwrite('test_transform.jpg',img_dilated)
  im2 = img.copy()
  max_area = 0
  xf, yf, wf, hf = 0,0,0,0
  for cnt in contours:
      x, y, w, h = cv2.boundingRect(cnt)
      area = w*h
      if(area > max_area):
        max_area = area
        xf,yf,wf,hf = x,y,w,h

  rect = cv2.rectangle(im2, (xf, yf), (xf + wf, yf + hf), (0, 255, 0), 2)
  cropped = im2[yf:yf + hf, xf:xf + wf]
  cv2.imwrite('test_boxes.jpg',im2)                                      

  return im2,cropped

get_bbox(cv2.imread('test4.png'))
     