from relinall.window import *

class Server(Window):

    def __init__(self):
        super().__init__()

        print("server")

        self.listServer()
    
    def listServer(self):
        self.serverData = QStandardItemModel()
        self.serverData.setHorizontalHeaderLabels(["Server List"])
        self.treeView.setModel(self.serverData)
        s = server()
        data = s.getServerGrouped()
        
        for group in data:
            serverGroup = QStandardItem(group.title())
            serverGroup.setData(json.dumps({'group':group, 'count': data[group]['count'] }))
            for host in data[group]['list']:
                serverDetails = QStandardItem(host['hostname'])
                serverDetails.setData(json.dumps({'hostname':host['hostname'], 'groupname': host['groupname'], 'username': host['username'], 'password': host['password'], 'port': host['port']}))
                serverGroup.appendRow(serverDetails)
            self.serverData.appendRow(serverGroup)
            
    def addServer(self):
        print("add server")
        msg = QMessageBox()
        msg.setText("This is a message box")
    
    def editServer(self):
        print("edit server")

    def removeServer(self):
        print("remove server")
