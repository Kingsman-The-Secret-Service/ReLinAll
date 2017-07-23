from relinall.window import *

class Summary(Window):

	def __init__(self):
		super().__init__()
		print("summary")

	def summary(self):

		self.serverDock()
		self.featureTab('summary')
