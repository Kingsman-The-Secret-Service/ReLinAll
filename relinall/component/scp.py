from relinall.window import *

class Scp(Window):

	def __init__(self):
		super().__init__()
		print("scp")

	def scp(self):

		self.docker('scp')
