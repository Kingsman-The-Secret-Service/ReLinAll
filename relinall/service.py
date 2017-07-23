from relinall.window import *

class Service(Window):

    def __init__(self):
        super().__init__()
        print("Service")

    def service(self):

        self.serverDock()
        self.featureTab('service')