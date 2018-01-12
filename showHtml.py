import sys
import time
import threading
import browser
import myEvent
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtWebKitWidgets import *
#
# app = QApplication(sys.argv)
#
#
# url='http://www.baidu.com/s?wd=我'
# browser = QWebView()
# browser.load(QUrl(url))
# browser.show()
#
# app.exec_()


# app = browser.QApplication(sys.argv)
# # 创建主窗口
# window = browser.MainWindow()
# # 显示窗口
# window.show()
# # 运行应用，并监听事件
# app.exec_()
# time.sleep(5)
# app.change_url("www.bing.com")


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        # print('into thread')
        app = browser.QApplication(sys.argv)
        print(app)
        window = browser.MainWindow()
        # 显示窗口
        window.show()
        self.window =window
        self.myApp = app
        print(window)
        print('info:thread '+str(self.threadID)+' is running')
        app.exec_()
    # def run_web_view(self):


class ShowHtml():
    def __init__(self):
        self.thread = myThread(1,"thread1", 1)
        # self.threads.append(myThread(2, "thread2", 2))
        # self.threads.append(myThread(3, "thread3", 3))
        self.thread.start()
        # time.sleep(2)
        # self.threads[1].start()
        # time.sleep(2)
        # self.threads[2].start()

    def setUrl(self,sword):
        url = u'http://www.baidu.com/s?wd='+str(sword)+' '
        # self.thread.window.change_url(url)
        QApplication.postEvent(self.thread.window, myEvent.MyEvent(url))
        # print('send over event')






