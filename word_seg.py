import cv2
import numpy as np
from utils import *
# 动态适应不同的输入图像大小
# 输入图像应为整个手机截屏图



img1 = cv2.imread('4.PNG',flags=cv2.IMREAD_GRAYSCALE)
x = 50
y = 300
w = 650
h = 150
crop_img1 = img1[y:y+h,x:x+w] #img[y: y + h, x: x + w]
height,width = crop_img1.shape
cv2.imshow('1',crop_img1)

kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(crop_img1,kernel,iterations = 1)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
th = cv2.threshold(dilation,thresh=200,maxval=255,type=cv2.THRESH_BINARY_INV)
_, contours0, hierarchy  = cv2.findContours(th[1],mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_SIMPLE)

contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
vis = np.zeros((height, width, 3), np.uint8)
vis2 = crop_img1.copy()
vis3 = crop_img1.copy()
vis4 = crop_img1.copy()
# vis2 =
img_with_contours = cv2.drawContours(vis, contours, -1, (255, 0, 255), 3, cv2.LINE_AA, hierarchy)

all_rects = []
for c in contours:
    pts = cv2.boundingRect(c)
    rect = coordinate_transfer(pts)
    all_rects.append(rect)

vis2 = draw_rects(vis2,all_rects)


while True:
    found_interaction = False
    for i in range(len(all_rects)-1):
        for j in range(i+1,len(all_rects)):
            r1 = all_rects[i]
            r2 = all_rects[j]
            if rect_interaction(r1,r2) > 0:#若相交
                print('发现相交')
                new_r = merge_rects(r1,r2)
                del all_rects[j]
                del all_rects[i]
                all_rects.append(new_r)
                found_interaction = True
                break
    print('====')
    if not found_interaction:
        break

cv2.imshow('origin vis4',vis4)
vis3 = draw_rects(vis3,all_rects)

all_rects = reduce_rects(all_rects,thresh_area=100)
# vis4 = draw_rects(vis4,all_rects)
cv2.imshow('2',erosion)
cv2.imshow('3',dilation)
cv2.imshow('4',th[1])
cv2.imshow('contours', img_with_contours)
cv2.imshow('rect',vis2)
cv2.imshow('mergerect',vis3)
cv2.imshow('reducerect',vis4)
cv2.waitKey()
