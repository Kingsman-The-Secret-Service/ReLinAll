from relinall.window import *

class Os(Window):

    def __init__(self):
        ssh = Helper.getData(self.widgetData[self.currentData()['hostname']], 'ssh')


	def changeDirectory(self):
        return 'cd'

    def listDirectory(self):
        return 'ls'

    def getHostname(self):
        return 'hostname'


class Rpm(Os):
    pass

class Debian(Os):
    pass

class Centos(Rpm):
    pass

class Redhat(Rpm):
    pass

class Ubuntu(Debian):
    pass

class Debian(Debian):
    pass

class Centos6(Centos):
    pass

class Centos7(Centos):
    pass

