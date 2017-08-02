from relinall.window import *

class Group(object):

	def __init__(self):
		super().__init__()

	def removeGroup(self):

		groupname = self.currentData()['groupname']
		reply = QMessageBox.question(self.MainWindow, 'Message', "Deleting the group <b>" + groupname + "</b> delete all server from it, are you sure wanna do it?", QMessageBox.Yes, QMessageBox.Close)

		if reply == QMessageBox.Yes:
			self.serverModel.deleteGroup(groupname)
			self.listServer()