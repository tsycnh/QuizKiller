import screen_grab
from pynput import keyboard
from PIL import ImageGrab
import QuizReader
import time
from myClient import *
from win32api import GetSystemMetrics
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import myEvent
import sys
import os

# mShowHtml = showHtml.ShowHtml()

class QuizKiller():
    def __init__(self):
        # self.box = (100, 200)  #width height
        self.sWidth = GetSystemMetrics(0)
        self.sHeight = GetSystemMetrics(1)
        self.qr = QuizReader.QuizReader()
        self.pic_index =0
        print("info:load over")
    def getScreenImage(self):

        #冲顶大会
        box = (self.sWidth-720,65,self.sWidth,self.sHeight-95)

        im = ImageGrab.grab()
        # im.save(addr)
        #box = (100, 100, 500, 500)
        region = im.crop(box)
        # region.show()
        self.pic_index = self.pic_index+1
        # region.save('aa.jpg')
        return region

    def runOCR(self,sImage):
        #sImage.show()

        t0 = time.time()
        # image = Image.open('2.PNG')
        try:
            s = self.qr.run(sImage)
        except:
            print('error:OCR算法出错')
            return list()
        t1 = time.time()
        print('s:', s)
        print('图像识别耗时：', t1 - t0)
        # text = '请问海贼王是谁写的'
        # text1 = '村上春树'
        # text2 = '尾田荣一郎'
        # text3 = '岸本齐史'
        # texts = list()
        # texts.append(text)
        # texts.append(text1)
        # texts.append(text2)
        # texts.append(text3)
        #
        # print('running OCR')
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
        dstROI = self.getScreenImage()
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
        self.killer = QuizKiller()
        self.initUI()
        print('load model over')

    def initUI(self):

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle("QuizKiller")
        self.show()

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
        try:
            if e.key() == Qt.Key_4:
                self.killer.quizSearch(self.killer.textlist, '1')
            if e.key() == Qt.Key_5:
                self.killer.quizSearch(self.killer.textlist, '2')
            if e.key() == Qt.Key_6:
                self.killer.quizSearch(self.killer.textlist, '3')
        except:
            print('warning：没有待搜索内容')
        if e.key() == Qt.Key_S:
            dstROI = self.killer.getScreenImage()
            curPath = os.getcwd()
            if False == os.path.exists(curPath+'/savedPic'):
                os.mkdir('savedPic')
            filename ='savedPic/'+ str(self.killer.pic_index)+'.jpg'
            print('info:saving pic')
            try:
                dstROI.save(filename,quality = 100)
            except:
                print("error:保存pic出错")

def main():
    app = QApplication(sys.argv)
    window = appQuizKiller()
    # window.show()
    app.exec_()

if __name__ == "__main__":
	main()