import cv2
import numpy as np
img = cv2.imread('crop2.jpg')

mser = cv2.MSER_create(_min_area=50)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((3, 3), np.uint8)
erosion = cv2.erode(gray, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=1)
th = cv2.threshold(dilation, thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)

regions, boxes = mser.detectRegions(th[1])
for box in boxes:
    x, y, w, h = box
    cv2.rectangle(img, (x,y),(x+w, y+h), (255, 0, 0), 2)
cv2.imshow('th',th[1])
cv2.imshow('brg',img)
cv2.waitKey()