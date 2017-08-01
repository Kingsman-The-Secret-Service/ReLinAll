from relinall.window import *
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from bash_kernel.kernel import *

class Putty(Window):

	def __init__(self):
		super().__init__()
		print("Putty")

	def putty(self):

		self.docker('putty')
		puttyTab = Helper.getData(self.widgetData[self.currentData()['hostname']], 'putty')

		layout = QVBoxLayout(puttyTab)

		self.process = QProcess()
		terminal = QWidget()

		# print(puttyTab, terminal, process)
		self.process.start('xterm', ['-into', str(terminal.winId())])
		# term = QWidget()
		layout.addWidget(terminal)

		# self.put_ipy(puttyTab)

	def port(self):

		self.serialPort = QtWidgets.QSerialPort(self.puttyTab)

		

	def put_ipy(self, parent):
		print("ff")
		kernel_manager = QtInProcessKernelManager()
		kernel_manager.start_kernel()
		kernel = kernel_manager.kernel
		kernel.gui = 'qt'

		kernel_client = kernel_manager.client()
		kernel_client.start_channels()
		kernel_client.namespace  = parent

		def stop():
			kernel_client.stop_channels()
			kernel_manager.shutdown_kernel()

		layout = QVBoxLayout(parent)
		widget = RichJupyterWidget(parent=parent)
		layout.addWidget(widget)
		widget.kernel_manager = kernel_manager
		widget.kernel_client = kernel_client
		widget.exit_requested.connect(stop)
		ipython_widget = widget
		ipython_widget.show()
		kernel.shell.push({'widget':widget,'kernel':kernel, 'parent':parent})
		return {'widget':widget,'kernel':kernel}

		

		