from PyQt5.QtCore import *

class MyEvent(QEvent):
    idType = QEvent.registerEventType()
    def __init__(self, data):
        QEvent.__init__(self, MyEvent.idType)
        self.data = data
    def get_data(self):
        return self.data






