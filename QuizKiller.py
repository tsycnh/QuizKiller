#!/usr/bin/python
import screen_grab
from pynput import keyboard
from PIL import ImageGrab
from QuizReader import QuizReader
# import cv2
import time
from myClient import *
try:
    from win32api import GetSystemMetrics
except:
    import wx

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton,QWidget,QApplication,QComboBox
import myEvent
import sys
import os

# mShowHtml = showHtml.ShowHtml()

class Setting:
    android_cd_setting = {
        'quiz':{
            'name':'冲顶大会',
            'question': {
                'x1': -500 / 720,  # 用来设置question的位置，前三个相对logo位置，y2相对answer位置
                'x2': 120 / 720,
                'y1': 170 / 1280,
                'y2': -50 / 1280,
            },
            'answer1': {'x1': 0.052, 'x2': 0.809, 'y1': 0.016, 'y2': 0.063},
            'answer2': {'x1': 0.054, 'x2': 0.808, 'y1': 0.101, 'y2': 0.146},
            'answer3': {'x1': 0.051, 'x2': 0.797, 'y1': 0.185, 'y2': 0.23}
        },
        'logo': './QuizReader/cd_logo_android.jpg',
        'answer':'./QuizReader/cd_answer_android.jpg',
        'width': 720,
        'height': 1280,
        'reduce_threshold':50/750,#删掉过小的bbox，此值越小，保留的最小bbox就会越小
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
        'logo': './QuizReader/bw_logo_apple.png',
        'answer':'',
        'width': 750,
        'height': 1334,
        'reduce_threshold':50/750,#删掉过小的bbox，此值越小，保留的最小bbox就会越小
        'confidence_threshold':0.7,#高于此置信度的文字才会被输出
    }


class QuizKiller():
    def __init__(self):
        # self.box = (100, 200)  #width height
        try:
            self.sWidth = GetSystemMetrics(0)
            self.sHeight = GetSystemMetrics(1)
        except:
            # app = wx.App(False)
            self.sWidth,self.sHeight = 1440,900# wx.GetDisplaySize()
        self.qr = QuizReader.QuizReader(Setting.android_cd_setting,'Source/chnData_resnet_20180113_1.h5','Source/source.txt')
        self.pic_index =0
        self.textlist = ['测试题干','选项1','选项2','选项3']
        print("info:load over")
    def getScreenImage(self):

        box = (self.sWidth-720,65,self.sWidth,self.sHeight-95)
        im = ImageGrab.grab()
        region = im.crop(box)
        self.pic_index = self.pic_index+1
        return region

    def runOCR(self,sImage):
        #sImage.show()

        t0 = time.time()
        s = self.qr.run(sImage)
        t1 = time.time()
        print('s:', s)
        print('图像识别耗时：', t1 - t0)

        self.textlist = s
        return s

    def quizSearch(self,texts,type):

        mC1 = mClient()
        mC2 = mClient()
        mC3 = mClient()

        if type==1:
            if mC1.connect(9000):
                mC1.send_data(texts[0])
        if type==2:
            if mC1.connect(9000):
                mC1.send_data(texts[1])
            if mC2.connect(9001):
                mC2.send_data(texts[2])
            if mC3.connect(9002):
                mC3.send_data(texts[3])
        if type==3:
            if mC1.connect(9000):
                mC1.send_data(texts[0]+' '+texts[1])
            if mC2.connect(9001):
                mC2.send_data(texts[0]+' '+texts[2])
            if mC3.connect(9002):
                mC3.send_data(texts[0]+' '+texts[3])


    def runQuizKiller(self,char):
        # print('into get image'+char)
        dstROI = self.getScreenImage()
        print('get image over')
        # dstROI.show()
        texts = self.runOCR(dstROI)
        print(texts)
        try:
            self.quizSearch(texts,int(char))
        except:
            print('error：搜索出错了')
class mrun():
    def __init__(self):
        self.killer = QuizKiller()
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

    def on_press(self,key):
        try:
            if key.char == '1' or key.char == '2' or key.char == '3':
                # qk = QuizKiller()
                self.killer.runQuizKiller(key.char)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))

    def on_release(self,key):
        #print('{0} released'.format(
        #    key))
        if key == keyboard.Key.esc:
        # Stop listener
            return False

class appQuizKiller(QWidget):
    def __init__(self):
        super().__init__()
        self.phoneSystem = '安卓系统'
        self.quizAppName = '冲顶大会'
        self.setting = Setting()
        self.killer = QuizKiller()
        self.initUI()
        print('load model over')
        self.show()
    def initUI(self):

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("QuizKiller")
        # self.show()

        btn = QPushButton('应用',self)
        btn.resize(btn.sizeHint())
        btn.move(100,210)
        btn.clicked.connect(self.applySetting)

        combo1 = QComboBox(self)
        combo1.addItem("安卓系统")
        combo1.addItem("苹果系统")
        combo1.setCurrentIndex(0)
        combo1.move(100,90)
        combo1.activated[str].connect(self.onActivated1)

        combo2 = QComboBox(self)
        combo2.addItem("冲顶大会")
        combo2.addItem("百万英雄")
        combo2.addItem("芝士超人")
        combo2.setCurrentIndex(0)
        combo2.move(100,150)
        combo2.activated[str].connect(self.onActivated2)

    def applySetting(self):#按钮的消息响应函数
        print('button')
        if self.phoneSystem == '安卓系统' and self.quizAppName == '冲顶大会':
            self.killer.qr.load_setting(self.setting.android_setting)
            return
        if self.phoneSystem == '苹果系统' and self.quizAppName == '百万英雄':
            self.killer.qr.load_setting(self.setting.apple_bw_setting)
            return
        print('没有适配')

    def onActivated1(self,text):#下拉菜单1的消息响应函数
        print('select '+text)
        self.phoneSystem = text

    def onActivated2(self, text):#下拉菜单2的消息响应函数
        print('select ' + text)
        self.quizAppName = text

    def savePic(self):
        dstROI = self.killer.getScreenImage()
        curPath = os.getcwd()
        if False == os.path.exists(curPath + '/savedPic'):
            os.mkdir('savedPic')
        filename = 'savedPic/' + str(self.killer.pic_index) + '.jpg'
        print('info:saving pic')
        try:
            dstROI.save(filename, quality=100)
        except:
            print("error:保存pic出错")

    def customEvent(self, e):
        if e.type() == myEvent.MyEvent.idType:
            print('e.event')

    def keyPressEvent(self, e):
        print('info:press '+str(e.key()))
        try:
            if e.key() == Qt.Key_1:
                self.killer.runQuizKiller('1')
            if e.key() == Qt.Key_2:
                self.killer.runQuizKiller('2')
            if e.key() == Qt.Key_3:
                self.killer.runQuizKiller('3')
        except:
            print('error：有一些错误')
        # if e.key() == Qt.Key_1:
        #     self.killer.runQuizKiller('1')
        try:
            if e.key() == Qt.Key_4:
                self.killer.quizSearch(self.killer.textlist, 1)
            if e.key() == Qt.Key_5:
                self.killer.quizSearch(self.killer.textlist, 2)
            if e.key() == Qt.Key_6:
                self.killer.quizSearch(self.killer.textlist, 3)
        except:
            print('warning：没有待搜索内容')
        if e.key() == Qt.Key_S:
            self.savePic()

def main():
    app = QApplication(sys.argv)
    window = appQuizKiller()
    # window.show()
    app.exec_()

if __name__ == "__main__":
	main()