import socket
import sys
import threading
import showHtml
import browser
from PyQt5.QtWidgets import *
import myEvent

class netThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter,window):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.window = window

    def run(self):
        # print('into thread')
        server = myServer(self.window)
        server.recMsg()
    # def run_web_view(self):


class myServer:
    HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
    # PORT = 9000  # Arbitrary non-privileged port

    def __init__(self,window):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.showHtml = showHtml.ShowHtml()
        self.PORT = int(sys.argv[1][0:])
        self.window =  window
        try:
            self.s.bind((self.HOST, self.PORT))
            print("info:listening:"+str(self.PORT))
        except socket.error as msg:
            print(msg)
            sys.exit()
        self.s.listen()
    def recMsg(self):
        while 1:
            # wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            bData = conn.recv(1024)
            # print(bData)
            msg = str(bData, "utf-8")
            print(msg)
            url = u'http://www.baidu.com/s?wd=' + str(msg) + ' '
            QApplication.postEvent(self.window, myEvent.MyEvent(url))


def main():
    app = browser.QApplication(sys.argv)
    window = browser.MainWindow()
    window.show()
    print('thread is running')

    thread = netThread(1, "thread1", 1,window=window)
    thread.start()

    app.exec_()
if __name__ == "__main__":
    main()