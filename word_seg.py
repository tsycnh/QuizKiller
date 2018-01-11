import cv2
import numpy as np
from utils import *
# 动态适应不同的输入图像大小
# 输入图像应为整个手机截屏图

class QuizReader:
    def __init__(self):
        pass
    def run(self,img_path):# 输入为手机截屏图像路径
        self.origin_img = cv2.imread(img_path)
        self.origin_img_gray = cv2.cvtColor(self.origin_img,code=cv2.COLOR_BGR2GRAY)
        self.line_height = (40/1334)*self.origin_img_gray.shape[0] #行间距
        self.crop_ROI()
        self.extract_bbox()
        self.sort_rects()
        self.get_single_words()

    # 切割题目区域
    def crop_ROI(self):
        self.crop_coordinates = {
            'x':int((50/750)*self.origin_img_gray.shape[1]),
            'y':int((300/1334)*self.origin_img_gray.shape[0]),
            'w':int((650/750)*self.origin_img_gray.shape[1]),
            'h':int((150/1334)*self.origin_img_gray.shape[0])
        }

        x = self.crop_coordinates['x']
        y = self.crop_coordinates['y']
        h = self.crop_coordinates['h']
        w = self.crop_coordinates['w']
        self.crop_img = self.origin_img_gray[y:y + h, x:x + w]  # img[top: bottom, left: right]
    # 获取每个文字的bbox
    def extract_bbox(self):
        height, width = self.crop_img.shape

        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(self.crop_img, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        th = cv2.threshold(dilation, thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)
        _, contours0, hierarchy = cv2.findContours(th[1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
        vis = np.zeros((height, width, 3), np.uint8)
        vis2 = self.crop_img.copy()
        vis3 = self.crop_img.copy()
        vis4 = self.crop_img.copy()

        img_with_contours = cv2.drawContours(vis, contours, -1, (255, 0, 255), 3, cv2.LINE_AA, hierarchy)

        all_rects = []
        for c in contours:
            pts = cv2.boundingRect(c)
            rect = coordinate_transfer(pts)
            all_rects.append(rect)

        vis2 = draw_rects(vis2, all_rects)

        while True:
            found_interaction = False
            for i in range(len(all_rects) - 1):
                for j in range(i + 1, len(all_rects)):
                    r1 = all_rects[i]
                    r2 = all_rects[j]
                    if rect_interaction(r1, r2) > 0:  # 若相交
                        print('发现相交')
                        new_r = merge_rects(r1, r2)
                        del all_rects[j]
                        del all_rects[i]
                        all_rects.append(new_r)
                        found_interaction = True
                        break
            print('====')
            if not found_interaction:
                break

        vis3 = draw_rects(vis3, all_rects)

        self.all_rects = reduce_rects(all_rects, thresh_area=100)
        vis4 = draw_rects(vis4,all_rects)

        cv2.imshow('1', self.crop_img)
        # cv2.imshow('2', erosion)
        # cv2.imshow('3', dilation)
        # cv2.imshow('4', th[1])
        # cv2.imshow('contours', img_with_contours)
        # cv2.imshow('origin vis4', vis4)
        # cv2.imshow('rect', vis2)
        # cv2.imshow('mergerect', vis3)
        cv2.imshow('reducerect', vis4)
        # cv2.waitKey()

    # 按照文字的纵向位置排序
    def sort_by_y(self,rects):
        return sorted(rects,key=lambda x:(x[3]+x[1])/2)
    # 按照文字的横向位置排序
    def sort_by_x(self,rects):
        return sorted(rects,key=lambda x:(x[0]+x[2])/2)
    # 将所有文字框排成一行
    def sort_rects(self):
        self.all_rects = self.sort_by_y(self.all_rects)
        y_gradients = []
        y_value=[]
        for i in range(len(self.all_rects)-1):
            g = self.all_rects[i+1][1]-self.all_rects[i][1]
            y_value.append(self.all_rects[i][1])
            y_gradients.append(g)
        print(self.all_rects)
        print(y_value)
        print(y_gradients)

        max_y = max(y_gradients)
        if max_y > self.line_height:# 分行
            max_y_index = y_gradients.index(max_y)
            line1 = self.all_rects[0:max_y_index+1]
            line2 = self.all_rects[max_y_index+1:]
            line1 = self.sort_by_x(line1)
            line2 = self.sort_by_x(line2)
            line1.extend(line2)
            self.all_rects =line1
        else:
            self.all_rects = self.sort_by_x(self.all_rects)

    def get_single_words(self):

        for rect in self.all_rects:
            word = self.crop_img[rect[1]:rect[3],rect[0]:rect[2]]
            cv2.imshow('word',word)
            cv2.waitKey()
            cv2.destroyWindow('word')

qr = QuizReader()
qr.run('5.PNG')

exit()
