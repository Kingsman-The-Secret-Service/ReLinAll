from relinall.window import *

class Remote(Window):

    def __init__(self):
        super().__init__()
        print("Remote")

    def remote(self):

        self.serverDock()
        self.featureTab('remote')