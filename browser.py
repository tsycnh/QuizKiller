# v1.2
# created
#   by Roger
# in 2017.1.3

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtGui import QKeyEvent

import sys
import myEvent

class MainWindow(QMainWindow):
    # noinspection PyUnresolvedReferences
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置窗口标题
        self.setWindowTitle('My Browser')
        # 设置窗口图标
        self.setWindowIcon(QIcon('icons/penguin.png'))
        # 设置窗口大小900*600
        self.resize(900, 600)
        self.show()

        # 设置浏览器
        self.browser = QWebView()
        url = u'http://www.baidu.com/s?wd=中国'
        # 指定打开界面的 URL
        self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        self.setCentralWidget(self.browser)


        ###使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(16, 16))
        #添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        #QAction类提供了抽象的用户界面action，这些action可以被放置在窗口部件中
        # 添加前进、后退、停止加载和刷新的按钮
        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
        stop_button = QAction(QIcon('icons/cross.png'), 'stop', self)
        reload_button = QAction(QIcon('icons/renew.png'), 'reload', self)

        back_button.triggered.connect(self.browser.back)
        next_button.triggered.connect(self.browser.forward)
        stop_button.triggered.connect(self.browser.stop)
        reload_button.triggered.connect(self.browser.reload)

        # 将按钮添加到导航栏上
        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(stop_button)
        navigation_bar.addAction(reload_button)

        #添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        #让浏览器相应url地址的变化
        self.browser.urlChanged.connect(self.renew_urlbar)
        self.url=''
        self.renew_f = False
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.browser.setUrl(q)
        # print('return to'+self.urlbar.text())
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
    def change_url(self,url):
        # self.setWindowFlags(state=[Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint])

        # self.show()
        # self.activateWindow()
        # self.raise_()
        # if self.browser.loadFinished()==False:


        q=QUrl(url)
        if q.scheme() == '':
            q.setScheme('http')
        try:
            self.browser.stop()
            self.browser.setUrl(q)
        except:
            print("brower..error")
        # self.browser.setUrl(q)
        # self.renew_urlbar(q)
        # self.url =url
        # self.navigate_to_url()
        # if self.renew_f == False:
        #     self.renew_f = True
        # self.navigate_to_url()
        # self.browser.load(q)
        # self.browser.show()

         # self.browser = QWebView()
        # url = u'http://www.baidu.com/s?wd=中国'
        # 指定打开界面的 URL
        # self.browser.setUrl(QUrl(url))
        # 添加浏览器到窗口中
        # self.setCentralWidget(self.browser)
        # self.browser.keyPressEvent()
        # self.browser.reload()
        # qe = QKeyEvent(type = )
        # self.urlbar.keyPressEvent(a0=qe)
        #self.browser.setHtml('aa',baseUrl=q)
        #evt = QKeyEvent(key=32,type=QEvent.Type)
        #self.urlbar.returnPressed()
        # self.navigate_to_url()
        print('set '+url)
    # def keyPressEvent(self, a0):
    #     # self.browser.setUrl(QUrl('https://www.baidu.com/s?wd=你好'))
    #     print('entering---------')
    # def enterEvent(self, a0):
    #     q = QUrl(self.url)
    #     if self.renew_f == True:
    #         if self.url != '':
    #             if q.scheme() == '':
    #                 q.setScheme('http')
    #             self.browser.setUrl(q)
    #         self.renew_f = False
    def customEvent(self, e):
        if e.type() == myEvent.MyEvent.idType:
            data = e.get_data()
            # self.change_url()
            self.change_url(str(data))
            print('custom event:'+data)

# # 创建应用
# app = QApplication(sys.argv)
# # 创建主窗口
# window = MainWindow()
# # 显示窗口
# window.show()
# # 运行应用，并监听事件
# app.exec_()