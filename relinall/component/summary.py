from relinall.window import *

class Summary(Window):

	def __init__(self):
		super().__init__()
		print("summary")

	def summary(self):

		self.docker('summary')

		tab = Helper.getData(self.widgetData[self.currentData()['hostname']], 'tab')
		ssh = Helper.getData(self.widgetData[self.currentData()['hostname']], 'ssh')
		print(tab, ssh)

		cmd = "ls -la"

		Ssh.execute(ssh, cmd)
		
        # tab.setLayout(QVBoxLayout())

        # label = QLabel('time')
        # label.setText(QDateTime.currentDateTime().toString())
        # tab.layout().addWidget(label)
