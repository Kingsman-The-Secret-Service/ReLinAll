from relinall.component.summary import *
from relinall.component.service import *
from relinall.component.putty import *
from relinall.component.ftp import *

class Component(Summary, Service, Putty, Ftp):
	def __init__(self):
		super().__init__()

from relinall.collator.server import *
from relinall.collator.group import *

class  Collator(Server, Group):
	def __init__(self):
		super().__init__()

class App(Component, Collator):

    def __init__(self):
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(QPixmap('icon.png')))
        super().__init__()
        sys.exit(app.exec_())

if __name__ == "__main__":
	App()
