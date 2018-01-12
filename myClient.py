


from QuizKiller import *
import socket

class mClient():

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_ip='127.0.0.1'
        # self.port
    def connect(self,port):
        try:
            self.s.connect((self.remote_ip, port))
            print('connected server:'+str(port))
        except socket.error as msg:
            print(msg)
            return False
        return True

    def send_data(self,data_str):
        bdata = bytes(data_str, 'utf-8')
        # print(bdata)
        len = 0
        while 1:
            len = self.s.sendall(bdata[len:])
            if not len:
                break
    # def send


# def main():
#     # with keyboard.Listener(
#     #         on_press=on_press,
#     #         on_release=on_release) as listener:
#     #     listener.join()
#     mC1 = mClient()
#     mC2 = mClient()
#     mC3 = mClient()
#
#     if mC1.connect(9000):
#         mC1.send_data("竹林七贤4")
#
#     if mC2.connect(9001):
#         mC2.send_data("竹林七贤5")
#
#     if mC3.connect(9002):
#         mC3.send_data("竹林七贤6")


# if __name__ == "__main__":
#
#     main()
