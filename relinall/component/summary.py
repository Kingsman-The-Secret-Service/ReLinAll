from relinall.window import *

class Summary(Window):

	summaryData = {}

	def __init__(self):
		super().__init__()

	def summary(self):

		self.docker('summary')

		# if 'summary' in self.widgetData[currentData['hostname']]:

		summaryTab = Helper.getData(self.widgetData[self.currentData()['hostname']], 'summary')
		ssh = Helper.getData(self.widgetData[self.currentData()['hostname']], 'ssh')
		summaryTab.setLayout(QVBoxLayout())

		self.ip()
		self.hostname(ssh)
		self.uptime(ssh)
		self.kernelname(ssh)
		self.kernelrelease(ssh)
		self.osname(ssh)
		self.processor(ssh)
		self.memory(ssh)
		# self.ifconfig()
		self.filesystem(ssh)
		self.release(ssh)

		html = self.render('summary.html', self.summaryData)
		view = QWebEngineView()
		view.setHtml(html,QUrl("file://"))
		summaryTab.layout().addWidget(view)


	def ip(self):
		self.summaryData['ip'] = self.currentData()['hostname']

	def hostname(self, ssh):
		output = Ssh.execute(ssh, 'hostname')
		self.summaryData['hostname'] = output.decode('utf-8')

	def uptime(self, ssh):
		output = Ssh.execute(ssh, 'uptime -p')
		self.summaryData['uptime'] = output.decode('utf-8')

	def kernelname(self, ssh):
		output = Ssh.execute(ssh, 'uname -s')
		self.summaryData['kernelname'] = output.decode('utf-8')
	
	def kernelrelease(self, ssh):
		output = Ssh.execute(ssh, 'uname -r')
		self.summaryData['kernelrelease'] = output.decode('utf-8')
	
	def osname(self, ssh):
		output = Ssh.execute(ssh, 'uname -o')
		self.summaryData['osname'] = output.decode('utf-8')
	
	def processor(self, ssh):
		output = Ssh.execute(ssh, 'uname -p')
		self.summaryData['processor'] = output.decode('utf-8')

	def memory(self, ssh):
		
		output = Ssh.execute(ssh, 'free -mw')
		fieldnames = ['type', 'total', 'used', 'free', 'shared', 'buff', 'cache', 'available']
		data = {d['type']:d for d in Helper.outputParser(output,fieldnames=fieldnames)}

		self.summaryData['chart'] = json.dumps([
			{
		        'name': 'Used',
		        'data': [int(data['Mem:']['used']), int(data['Swap:']['used'])]
		    }, {
		        'name': 'Free',
		        'data': [int(data['Mem:']['free']), int(data['Swap:']['free'])]
		    }, {
		        'name': 'Buffer',
		        'data': [int(data['Mem:']['buff'])]
		    }, {
		        'name': 'Cache',
		        'data': [int(data['Mem:']['cache'])]
		    }
        ])

	def filesystem(self, ssh):
		output = Ssh.execute(ssh, 'df -h')
		fieldnames = ['filesystem', 'size', 'used', 'avail', 'use', 'mounted']
		data = [ d for d in Helper.outputParser(output,fieldnames=fieldnames)]

		self.summaryData['filesystem'] = data

	def ifconfig(self, ssh):
		output = Ssh.execute(ssh, 'ifconfig')
		parsed = Helper.outputParser(output)


	def release(self, ssh):
		output = Ssh.execute(ssh, 'cat /etc/*-release')
		fieldnames = ['field', 'value']
		data = { d['field'] : d['value'] for d in Helper.outputParser(output,delimiter='=',fieldnames=fieldnames)}
		self.summaryData['release'] = data
