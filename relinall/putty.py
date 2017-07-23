from relinall.window import *

class Putty(Window):

    def __init__(self):
        super().__init__()
        print("Putty")

    def putty(self):

        self.serverDock()
        self.featureTab('putty')

    def port(self):

        self.serialPort = QtWidgets.QSerialPort(self.puttyTab)