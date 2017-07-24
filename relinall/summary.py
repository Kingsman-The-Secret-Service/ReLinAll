from relinall.window import *

class Summary(Window):

	def __init__(self):
		super().__init__()
		print("summary")

	def summary(self):

		self.docker()
		self.tabber('summary')
		
        # tab.setLayout(QVBoxLayout())

        # label = QLabel('time')
        # label.setText(QDateTime.currentDateTime().toString())
        # tab.layout().addWidget(label)
