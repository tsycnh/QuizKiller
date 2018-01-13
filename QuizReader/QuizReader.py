import cv2
from PIL import Image
import numpy as np
from QuizReader.utils import *
import keras
import time
# 动态适应不同的输入图像大小
# 输入图像应为整个手机截屏图

class QuizReader:
    def __init__(self,setting,model_path,source_path):
        self.setting = setting
        self.load_model(model_path,source_path)
        # 当前设置适合冲顶大会
        # self.question_ratio={'x':0.0667,'y':0.2249,'w':0.8667,'h':0.1124}
        # self.answer1_ratio ={'x':0.12,'y':0.41,'w':0.7,'h':0.05}
        # self.answer2_ratio ={'x':0.12,'y':0.495,'w':0.7,'h':0.05}
        # self.answer3_ratio ={'x':0.12,'y':0.575,'w':0.7,'h':0.05}

    def load_model(self,model_path,source_path):
        keras.backend.clear_session()
        self.model = keras.models.load_model(model_path)
        word_dict = open(source_path).readlines()
        tmp_dict = []
        for w in word_dict:
            new_w = w.replace('\n','')
            tmp_dict.append(new_w)
        self.word_dict = tmp_dict

    def run(self,img):# 输入为手机截屏图像
        self.origin_img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
        print('origin shape',self.origin_img.shape)
        new_w = self.setting['width']
        new_h = int((new_w*self.origin_img.shape[0])/self.origin_img.shape[1])
        self.origin_img = cv2.resize(self.origin_img,(new_w,new_h))
        print('after shape',self.origin_img.shape)
        self.origin_img_gray = cv2.cvtColor(self.origin_img,code=cv2.COLOR_BGR2GRAY)
        self.line_height = (40/1334)*self.origin_img_gray.shape[0] #行间距
        q_coord = self.calc_question_coord()
        question = self.get_sentence_from_ROI(q_coord)
        # answer3 = self.get_sentence_from_ROI(self.answer3_ratio)
        # answer2 = self.get_sentence_from_ROI(self.answer2_ratio)
        # answer1 = self.get_sentence_from_ROI(self.answer1_ratio)

        return [question,'','','']

    def calc_question_coord(self):
        logo = cv2.imread(self.setting['logo'])  # img.shape => (h,w)
        answer = cv2.imread(self.setting['answer'])
        img = self.origin_img

        logo_h, logo_w, _ = logo.shape
        answer_h, answer_w, _ = answer.shape
        img_h, img_w, _ = img.shape
        r = cv2.matchTemplate(img, logo, method=cv2.TM_SQDIFF)
        r2 = cv2.matchTemplate(img, answer, method=cv2.TM_SQDIFF)
        logo_pos = cv2.minMaxLoc(r)[2]
        answer_pos = cv2.minMaxLoc(r2)[2]  # (540,70)=>(x,y)
        # print(img_w,img_h)# 720 1280
        x_logo = logo_pos[0]
        y_logo = logo_pos[1]
        y_a = answer_pos[1]
        x1 = int(x_logo + img_w * (self.setting['x1']))
        x2 = int(x_logo + img_w * (self.setting['x2']))
        y1 = int(y_logo + img_h * (self.setting['y1']))
        y2 = int(y_a + img_h * (self.setting['y2']))

        question_pos = (x1, y1, x2, y2)  # img[x1, y1, x2, y2]#左上角点，右下角点

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
    def get_sentence_from_ROI(self,coord):
        self.crop_ROI(coord)
        # cv2.imwrite('crop2.jpg',self.crop_img)
        # exit()
        self.extract_bbox()
        if len(self.all_rects)<=0:
            return ''
        elif len(self.all_rects)>1:
            self.sort_rects()
            # img = draw_rects(self.crop_img,self.all_rects)
            # cv2.imshow('aaa',img)
            # cv2.waitKey()
        self.get_single_words()
        if len(self.all_words)<=0:
            return ''
        return self.export_sentence()

    def export_sentence(self):
        def preprocess_input(x):# 归一化至-1～+1之间
            return ((x / 255) - 0.5) * 2

        images = []
        for img in self.all_words:
            p_img = preprocess_input(img)
            images.append(p_img)

        classes = self.model.predict(np.array(images), batch_size=len(self.all_words))

        sentence = ''
        print(classes.shape)
        for c in classes:
            index = np.argmax(c)
            confidence = np.amax(c)
            # print('置信度：',confidence)
            if confidence >= self.setting['confidence_threshold']:
                sentence+=self.word_dict[index]
        return sentence
        # print(classes)
    # 切割区域
    def crop_ROI(self,coord):
        x1,y1,x2,y2 = coord[0],coord[1],coord[2],coord[3]
        self.crop_img = self.origin_img_gray[y1:y2,x1:x2]  # img[top: bottom, left: right]
    # 获取每个文字的bbox
    def merge_line_y_rects(self,line_rects):
        while True:
            centers = []
            line_rects = self.sort_by_x(line_rects)
            for rect in line_rects:
                x_c = (rect[0]+rect[2])/2
                centers.append(x_c)
            g = self.calc_gradients(centers)
            min_gap = min(g)
            if min_gap <=10:
                index = g.index(min_gap)
                r1 = line_rects[index]
                r2 = line_rects[index+1]
                new_rect = merge_rects(r1,r2)
                del line_rects[index+1]
                del line_rects[index]
                line_rects.append(new_rect)
            else:
                break
        print('centers:',centers)
        print('gradients:',g)
        return line_rects
    def extract_bbox(self):
        height, width = self.crop_img.shape

        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(self.crop_img, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        th = cv2.threshold(dilation, thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)
        _, contours0, hierarchy = cv2.findContours(th[1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
        # vis = np.zeros((height, width, 3), np.uint8)
        # vis2 = self.crop_img.copy()
        # vis3 = self.crop_img.copy()
        # vis4 = self.crop_img.copy()

        # img_with_contours = cv2.drawContours(vis, contours, -1, (255, 0, 255), 3, cv2.LINE_AA, hierarchy)

        all_rects = []
        for c in contours:
            pts = cv2.boundingRect(c)
            rect = coordinate_transfer(pts)
            all_rects.append(rect)

        # vis2 = draw_rects(vis2, all_rects)

        while True:
            found_interaction = False
            for i in range(len(all_rects) - 1):
                for j in range(i + 1, len(all_rects)):
                    r1 = all_rects[i]
                    r2 = all_rects[j]
                    if rect_interaction(r1, r2) > 0:  # 若相交
                        # print('发现相交')
                        new_r = merge_rects(r1, r2)
                        del all_rects[j]
                        del all_rects[i]
                        all_rects.append(new_r)
                        found_interaction = True
                        break
            # print('====')
            if not found_interaction:
                break

        # vis3 = draw_rects(vis3, all_rects)

        self.all_rects = reduce_rects(all_rects, thresh_area=self.setting['reduce_threshold']*self.setting['width'])
        # vis4 = draw_rects(vis4,all_rects)

        # cv2.imshow('1', self.crop_img)
        # cv2.imshow('2', erosion)
        # cv2.imshow('3', dilation)
        # cv2.imshow('4', th[1])
        # cv2.imshow('contours', img_with_contours)
        # cv2.imshow('origin vis4', vis4)
        # cv2.imshow('rect', vis2)
        # cv2.imshow('mergerect', vis3)
        # cv2.imshow('reducerect', vis4)
        # cv2.waitKey()
    # 按照文字的纵向位置排序
    def sort_by_y(self,rects):
        return sorted(rects,key=lambda x:(x[3]+x[1])/2)
    # 按照文字的横向位置排序
    def sort_by_x(self,rects):
        return sorted(rects,key=lambda x:(x[0]+x[2])/2)
    # 将所有文字框排成一行
    def calc_gradients(self,list):
        gradients = []
        for i in range(len(list)-1):
            g = list[i+1]-list[i]
            gradients.append(g)
        return gradients
    def sort_rects(self):
        self.all_rects = self.sort_by_y(self.all_rects)
        y_gradients = []
        y_value=[]
        for i in range(len(self.all_rects)-1):
            g = self.all_rects[i+1][1]-self.all_rects[i][1]
            y_value.append(self.all_rects[i][1])
            y_gradients.append(g)
        # print(self.all_rects)
        # print(y_value)
        # print('y_gradients : ',y_gradients)

        max_y = max(y_gradients)
        if max_y > self.line_height:# 分行
            max_y_index = y_gradients.index(max_y)
            line1 = self.all_rects[0:max_y_index+1]
            line2 = self.all_rects[max_y_index+1:]
            line1 = self.merge_line_y_rects(line1)
            line2 = self.merge_line_y_rects(line2)

            #merge
            line1 = self.sort_by_x(line1)
            line2 = self.sort_by_x(line2)
            line1.extend(line2)
            self.all_rects =line1
        else:
            line = self.all_rects
            line = self.merge_line_y_rects(line)
            tmp = self.sort_by_x(line)
            self.all_rects =tmp

    def get_single_words(self,word_size=32):
        bg = np.zeros((word_size,word_size,1),dtype=np.uint8)
        bg += 255
        ratio = 0.9
        self.all_words = []
        i = 0
        for rect in self.all_rects:
            word = self.crop_img[rect[1]:rect[3],rect[0]:rect[2]]
            # self.crop_img[rect[1]:rect[3], rect[0]:rect[2]] = 0
            small_word = image_resize(word,32*ratio)
            canvas = bg.copy()
            w = small_word.shape[1]
            h = small_word.shape[0]
            x = int((word_size - small_word.shape[1])/2)
            y = int((word_size - small_word.shape[0])/2)
            canvas[y:y+h,x:x+w] = np.expand_dims(small_word,axis=2)
            finale = cv2.cvtColor(canvas,cv2.COLOR_GRAY2RGB)
            self.all_words.append(finale)

            # cv2.imwrite('test'+str(i)+'.jpg',finale)
            # # cv2.imshow('word',word)
            # # cv2.imshow('new word',small_word)
            # # cv2.imshow('word image',canvas)
            # # cv2.waitKey()
            # # cv2.destroyAllWindows()
            # i+=1

if __name__ == '__main__':
    android_setting = {
        'x1': -500 / 720,#用来设置question的位置
        'x2': 120 / 720,
        'y1': 170 / 1280,
        'y2': -50 / 1280,
        'logo': '冲顶logo_android.jpg',
        'answer': '冲顶answer_android.jpg',
        'width': 720,
        'height': 1280,
        'reduce_threshold':50/720,#删掉过小的bbox，此值越小，保留的最小bbox就会越小
        'confidence_threshold':0.7,#高于此置信度的文字才会被输出
    }
    qr = QuizReader(android_setting,'Source/chnData_resnet.h5','Source/source.txt')
    t0 = time.time()
    image = Image.open('test_images/冲顶1.jpg')

    s = qr.run(image)
    t1 = time.time()
    print('s:',s)
    print('图像识别耗时：',t1-t0)
    exit()
