import cv2
import numpy as np

android_setting = {
    'x1':-500/720,
    'x2':120/720,
    'y1':170/1280,
    'y2':-50/1280,
    'logo':'冲顶logo_android.jpg',
    'answer':'冲顶answer_android.jpg',
    'width':720,
    'height':1280
}
setting = android_setting

def calc_question_coord():
    logo = cv2.imread(setting['logo'])# img.shape => (h,w)
    answer = cv2.imread(setting['answer'])
    img = cv2.imread('test_images/1.PNG')

    logo_h,logo_w,_ = logo.shape
    answer_h,answer_w,_ = answer.shape
    img_h,img_w,_ = img.shape
    r = cv2.matchTemplate(img,logo,method=cv2.TM_SQDIFF)
    r2 = cv2.matchTemplate(img,answer,method=cv2.TM_SQDIFF)
    logo_pos=cv2.minMaxLoc(r)[2]
    answer_pos=cv2.minMaxLoc(r2)[2]# (540,70)=>(x,y)
    # print(img_w,img_h)# 720 1280
    x_logo = logo_pos[0]
    y_logo = logo_pos[1]
    y_a = answer_pos[1]
    x1 = int(x_logo + img_w * (setting['x1']))
    x2 = int(x_logo + img_w * (setting['x2']))
    y1 = int(y_logo + img_h * (setting['y1']))
    y2 = int(y_a + img_h * (setting['y2']))

    question_pos = (x1,y1,x2,y2)#img[x1, y1, x2, y2]#左上角点，右下角点

    # # print(anser_pos)
    # img[logo_pos[1]:logo_pos[1]+logo_h,logo_pos[0]:logo_pos[0]+logo_w] = np.zeros(logo.shape,dtype=np.uint8)## img[top: bottom, left: right]
    # img[answer_pos[1]:answer_pos[1] + answer_h, answer_pos[0]:answer_pos[0] + answer_w] = np.zeros(answer.shape, dtype=np.uint8)## img[top: bottom, left: right]
    # crop = img[y1:y2,x1:x2].copy()
    # img[y1:y2,x1:x2] = np.zeros((y2-y1,x2-x1,3),dtype=np.uint8)
    # # cv2.imshow('logo',logo)
    # cv2.imshow('img',img)
    # cv2.imshow('crop',crop)
    # # cv2.imwrite('mask.jpg',img)
    # cv2.waitKey()
    return question_pos