import socket
import sys
import threading
import showHtml



# class mySocketThread (threading.Thread):   #继承父类threading.Thread
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#
#     def run(self):
#         server = myServer()
#         server.recMsg()
#     # def run_web_view(self):

class myServer:
    HOST = '127.0.0.1'  # Symbolic name meaning all available interfaces
    # PORT = 9000  # Arbitrary non-privileged port

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.showHtml = showHtml.ShowHtml()
        self.PORT = int(sys.argv[1][0:])
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
            print(addr[0])
            print(addr[1])
            bData = conn.recv(1024)
            print(bData)
            msg = str(bData, "utf-8")
            print(msg)
            self.showHtml.setUrl(msg)


def main():
    server  = myServer()
    server.recMsg()

if __name__ == "__main__":
    main()