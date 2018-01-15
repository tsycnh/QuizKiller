# coding=utf-8
import cv2
from PIL import Image
import numpy as np
# from . import utils
try:
    from . import utils # "myapp" case
except:
    import utils # "__main__" case
import keras
import time
# 动态适应不同的输入图像大小
# 输入图像应为整个手机截屏图

class QuizReader:
    def __init__(self,setting,model_path,source_path):
        self.setting = setting
        self.debug = True
        if not self.debug:
            self.load_model(model_path,source_path)

    def load_model(self,model_path,source_path):
        keras.backend.clear_session()
        self.model = keras.models.load_model(model_path)
        word_dict = open(source_path,encoding='utf-8').readlines()
        tmp_dict = []
        for w in word_dict:
            new_w = w.replace('\n','')
            tmp_dict.append(new_w)
        self.word_dict = tmp_dict
    def load_setting(self,setting):
        self.setting = setting

    def run(self,img):# 输入为手机截屏图像
        self.origin_img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
        print('origin shape',self.origin_img.shape)
        new_w = self.setting['width']
        new_h = int((new_w*self.origin_img.shape[0])/self.origin_img.shape[1])
        self.origin_img = cv2.resize(self.origin_img,(new_w,new_h))
        print('after shape',self.origin_img.shape)
        self.origin_img_gray = cv2.cvtColor(self.origin_img,code=cv2.COLOR_BGR2GRAY)
        self.line_height = (40/1334)*self.origin_img_gray.shape[0] #行间距
        print('计算坐标')
        q_coord = self.calc_question_coord(ratio = self.setting['quiz']['question'])
        a1_coord = self.calc_coord(ratio = self.setting['quiz']['answer1'])
        a2_coord = self.calc_coord(ratio = self.setting['quiz']['answer2'])
        a3_coord = self.calc_coord(ratio = self.setting['quiz']['answer3'])
        print('获取语句')
        question = self.get_sentence_from_ROI(q_coord)
        answer1 = self.get_sentence_from_ROI(a1_coord)
        answer2 = self.get_sentence_from_ROI(a2_coord)
        answer3 = self.get_sentence_from_ROI(a3_coord)

        return question,answer1,answer2,answer3

    def calc_question_coord(self,ratio):
        if self.setting['quiz']['name'] == '冲顶大会':
            logo = cv2.imread(self.setting['logo'])  # img.shape => (h,w)
            answer = cv2.imread(self.setting['answer'])
            img = self.origin_img.copy()

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
            x1 = int(x_logo + img_w * (ratio['x1']))
            x2 = int(x_logo + img_w * (ratio['x2']))
            y1 = int(y_logo + img_h * (ratio['y1']))
            y2 = int(y_a + img_h * (ratio['y2']))

            question_pos = (x1, y1, x2, y2)  # img[x1, y1, x2, y2]#左上角点，右下角点
            return question_pos
        elif self.setting['quiz']['name'] == '百万英雄':
            logo = cv2.imread(self.setting['logo'])  # img.shape => (h,w)
            img = self.origin_img.copy()

            logo_h, logo_w, _ = logo.shape
            img_h, img_w, _ = img.shape
            r = cv2.matchTemplate(img, logo, method=cv2.TM_SQDIFF)
            logo_pos = cv2.minMaxLoc(r)[2]
            # print(img_w,img_h)# 720 1280
            x_logo = logo_pos[0]
            y_logo = logo_pos[1]
            x1 = int(x_logo + img_w * (ratio['x1']))
            x2 = int(x_logo + img_w * (ratio['x2']))
            y1 = int(y_logo + img_h * (ratio['y1']))
            y2 = int(y_logo + img_h * (ratio['y2']))

            question_pos = (x1, y1, x2, y2)  # img[x1, y1, x2, y2]#左上角点，右下角点
            return question_pos


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
    def calc_coord(self,ratio):
        if self.setting['quiz']['name'] == '冲顶大会':
            answer = cv2.imread(self.setting['answer'])
            img = self.origin_img.copy()
            answer_h, answer_w, _ = answer.shape
            img_h, img_w, _ = img.shape
            r2 = cv2.matchTemplate(img, answer, method=cv2.TM_SQDIFF)
            answer_pos = cv2.minMaxLoc(r2)[2]  # (540,70)=>(x,y)
            # print(img_w,img_h)# 720 1280
            x_a = answer_pos[0]
            y_a = answer_pos[1]

            x1 = int(x_a + img_w * (ratio['x1']))
            x2 = int(x_a + img_w * (ratio['x2']))
            y1 = int(y_a + img_h * (ratio['y1']))
            y2 = int(y_a + img_h * (ratio['y2']))

            pos = (x1, y1, x2, y2)  # img[x1, y1, x2, y2]#左上角点，右下角点

            # print(anser_pos)
            # img[answer_pos[1]:answer_pos[1] + answer_h, answer_pos[0]:answer_pos[0] + answer_w] = np.zeros(answer.shape, dtype=np.uint8)## img[top: bottom, left: right]
            #crop = img[y1:y2,x1:x2].copy()
            #img[y1:y2,x1:x2] = np.zeros((y2-y1,x2-x1,3),dtype=np.uint8)
            # cv2.imshow('img',img)
            # cv2.imshow('crop',crop)
            # # cv2.imwrite('mask.jpg',img)
            # cv2.waitKey()
            return pos
        elif self.setting['quiz']['name']=='百万英雄':
            pos = self.calc_question_coord(ratio)
            return pos

    def get_sentence_from_ROI(self,coord):
        print('ROI切割')
        self.crop_ROI(coord)
        if self.debug:
            cv2.imwrite('tmp/'+str(time.time())+'1首次ROI切割.jpg',self.crop_img)

        print('bbox提取')
        self.extract_bbox()
        if self.debug:
            img = utils.draw_rects(self.crop_img, self.all_rects)
            cv2.imwrite('tmp/'+str(time.time())+'2首次bbox提取.jpg',img)
        print('rects排序')
        if len(self.all_rects)<=0:
            return ''
        elif len(self.all_rects)>1:
            self.sort_rects()
            if self.debug:
                img = utils.draw_rects(self.crop_img,self.all_rects)
                cv2.imwrite('tmp/'+str(time.time())+'3rects排序后.jpg',img)

        print('文字图片生成')
        self.get_single_words()
        if len(self.all_words)<=0:
            print('--无文字--')
            return ''
        print('导出句子')
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
            else:
                sentence+='*'
        return sentence
        # print(classes)
    # 切割区域
    def crop_ROI(self,coord):
        x1,y1,x2,y2 = coord[0],coord[1],coord[2],coord[3]
        self.crop_img = self.origin_img_gray[y1:y2,x1:x2].copy()  # img[top: bottom, left: right]
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
                new_rect = utils.merge_rects(r1,r2)
                del line_rects[index+1]
                del line_rects[index]
                line_rects.append(new_rect)
            else:
                break
        print('centers:',centers)
        print('gradients:',g)
        return line_rects


    # 获取每个文字的bbox
    def extract_bbox(self):
        height, width = self.crop_img.shape

        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(self.crop_img.copy(), kernel, iterations=1)
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
            rect = utils.coordinate_transfer(pts)
            all_rects.append(rect)

        # vis2 = draw_rects(vis2, all_rects)
        utils.merge_group_rects(all_rects,gap=1)


        self.all_rects = utils.reduce_rects(all_rects, thresh_area=self.setting['reduce_threshold']*self.setting['width'])
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

    # 计算梯度
    def calc_gradients(self,list):
        gradients = []
        for i in range(len(list)-1):
            g = list[i+1]-list[i]
            gradients.append(g)
        return gradients

    # 规范同一行文字rect高度
    # 这里会直接对single_line_rects做修改
    def regulate_rect_heights(self,single_line_rects):
        y_top = min(single_line_rects,key=lambda x:x[1])[1]
        y_bottom = max(single_line_rects,key=lambda x:x[3])[3]
        for rect in single_line_rects:
            rect[1] = y_top
            rect[3] = y_bottom

    # 将所有文字框排成一行
    def sort_rects(self):
        self.all_rects = self.sort_by_y(self.all_rects)
        y_gradients = []
        y_value=[]
        for i in range(len(self.all_rects)-1):
            g = self.all_rects[i+1][1]-self.all_rects[i][1]
            y_value.append(self.all_rects[i][1])
            y_gradients.append(g)
        # print(self.all_rects)

        if self.debug:
            img = utils.draw_rects(self.crop_img,self.all_rects)
            cv2.imwrite('tmp/f_sort_rects_1.jpg',img)
            print(y_value)
            print('y_gradients : ',y_gradients)

        # max_y = max(y_gradients)
        max_y_index = utils.find_first_greater_value(self.line_height,y_gradients)
        other_rects = self.all_rects
        other_gradients = y_gradients
        all_lines = []
        if max_y_index>0:
            while max_y_index >0:
                line = other_rects[:max_y_index+1]
                other_rects = other_rects[max_y_index+1:]
                other_gradients = other_gradients[max_y_index+1:]
                all_lines.append(line)
                max_y_index = utils.find_first_greater_value(self.line_height,other_gradients)
            all_lines.append(other_rects)
        else:
            all_lines = [self.all_rects]
        for l in all_lines:
            self.regulate_rect_heights(l)

        single_lines =[]
        for single_line in all_lines:
            line = self.merge_line_y_rects(single_line)
            line = self.sort_by_x(line)
            single_lines.extend(line)

        self.all_rects = single_lines

    # 获取单行文字
    def get_single_words(self,word_size=32):
        bg = np.zeros((word_size,word_size,1),dtype=np.uint8)
        bg += 255
        ratio = 0.9
        self.all_words = []
        i = 0
        for rect in self.all_rects:
            word = self.crop_img[rect[1]:rect[3],rect[0]:rect[2]]
            # self.crop_img[rect[1]:rect[3], rect[0]:rect[2]] = 0
            small_word = utils.image_resize(word,32*ratio)
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
    android_bw_setting = {
        'name':'百万英雄',
        'quiz':{
            'question':{'x1': -0.744, 'x2': 0.126, 'y1': 0.156, 'y2': 0.333},
            'answer1':{'x1': -0.691, 'x2': -0.013, 'y1': 0.359, 'y2': 0.419},
            'answer2':{'x1': -0.672, 'x2': 0.019, 'y1': 0.457, 'y2': 0.525},
            'answer3':{'x1': -0.672, 'x2': 0.05, 'y1': 0.564, 'y2': 0.618}

        },
        'logo': 'bw_logo_android.jpg',
        'answer': '',
        'width': 1080,
        'height': 1920,
        'reduce_threshold':50/1080,#删掉过小的bbox，此值越小，保留的最小bbox就会越小
        'confidence_threshold':0.7,#高于此置信度的文字才会被输出
    }
    apple_bw_setting = {
        'quiz':{
            'name':'百万英雄',
            'question':{'x1': -0.71, 'x2': 0.14, 'y1': 0.163, 'y2': 0.332},
            'answer1':{'x1': -0.651, 'x2': 0.056, 'y1': 0.376, 'y2': 0.43},
            'answer2':{'x1': -0.641, 'x2': 0.061, 'y1': 0.476, 'y2': 0.526},
            'answer3':{'x1': -0.658, 'x2': 0.075, 'y1': 0.576, 'y2': 0.626}
        },
        'logo': 'bw_logo_apple.png',
        'answer':'',
        'width': 750,
        'height': 1334,
        'reduce_threshold':50/750,#删掉过小的bbox，此值越小，保留的最小bbox就会越小
        'confidence_threshold':0.7,#高于此置信度的文字才会被输出
    }
    qr = QuizReader(apple_bw_setting,'chnData_resnet.h5','source.txt')
    t0 = time.time()
    image = Image.open('test_images/苹果/百万英雄/1.png')

    s = qr.run(image)
    t1 = time.time()
    cv2.imshow('crop',qr.crop_img)
    print('s:',s)
    print('图像识别耗时：',t1-t0)
    cv2.waitKey()
    exit()
