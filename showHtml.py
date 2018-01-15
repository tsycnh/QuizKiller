import sys
import time
import threading
import browser
import myEvent
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        # print('into thread')
        app = browser.QApplication(sys.argv)
        window = browser.MainWindow()
        window.show()
        print('thread is running')
        app.exec_()
    # def run_web_view(self):


class ShowHtml():
    def __init__(self):
        self.thread = myThread(1,"thread1", 1)
        self.thread.start()


    def setUrl(self,sword):
        url = u'http://www.baidu.com/s?wd='+str(sword)+' '
        QApplication.postEvent(self.thread.window, myEvent.MyEvent(url))
        # print('send over event')






