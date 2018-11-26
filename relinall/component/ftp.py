from relinall.window import *

class Ftp(Window):

	def __init__(self):
		super().__init__()
		print("ftp")

	def ftp(self):

		self.docker('ftp')
