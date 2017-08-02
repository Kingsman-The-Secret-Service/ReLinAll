from relinall.window import *

class Server(Window):

    def __init__(self):
        super().__init__()
        self.listServer()
    
    def listServer(self):
        self.serverData = QStandardItemModel()
        self.serverData.setHorizontalHeaderLabels(["Server List"])
        self.treeView.setModel(self.serverData)
        self.serverModel = ServerModel()
        data = self.serverModel.getServerGrouped()
        
        for group in data:
            serverGroup = QStandardItem(group)
            serverGroup.setData(json.dumps({'groupname':group, 'count': data[group]['count'] }))
            for host in data[group]['list']:
                serverDetails = QStandardItem(host['hostname'])
                serverDetails.setData(json.dumps({'hostname':host['hostname'], 'groupname': host['groupname'], 'username': host['username'], 'password': host['password'], 'port': host['port']}))
                serverGroup.appendRow(serverDetails)
            self.serverData.appendRow(serverGroup)
            
    def addServer(self):

        if self.MainWindow.sender().objectName() == 'MainMenuAddServer':
            self.serverForm()
        else:
            self.serverForm(self.currentData())
    
    def editServer(self):
        self.serverForm(self.currentData())

    def serverForm(self, fieldValue = {}):

        # Server Dialog
        self.serverDialog = QDialog()
        self.serverDialog.setWindowTitle("Add Server Details")
        self.serverDialog.setWindowModality(Qt.ApplicationModal)
        self.serverDialog.setFixedSize(300,220)

        formWidget = QWidget(self.serverDialog)
        formLayout = QFormLayout(formWidget)

        groupLabel = QLabel(formWidget)
        groupLabel.setText('Group Name')
        formLayout.setWidget(0, QFormLayout.LabelRole, groupLabel)
        hostLabel = QLabel(formWidget)
        hostLabel.setText('Hostname / IP')
        formLayout.setWidget(1, QFormLayout.LabelRole, hostLabel)
        userLabel = QLabel(formWidget)
        userLabel.setText('Username')
        formLayout.setWidget(2, QFormLayout.LabelRole, userLabel)
        passLabel = QLabel(formWidget)
        passLabel.setText('Password')
        formLayout.setWidget(3, QFormLayout.LabelRole, passLabel)
        portLabel = QLabel(formWidget)
        portLabel.setText('Port Number')
        formLayout.setWidget(4, QFormLayout.LabelRole, portLabel)

        if 'groupname' in fieldValue:
            self.groupField = QComboBox(formWidget)
            formLayout.setWidget(0, QFormLayout.FieldRole, self.groupField)
            self.groupField.setModel(self.serverData)
        else:
            self.groupField = QLineEdit(formWidget)
            formLayout.setWidget(0, QFormLayout.FieldRole, self.groupField)

        self.hostField = QLineEdit(formWidget)
        formLayout.setWidget(1, QFormLayout.FieldRole, self.hostField)
        self.userField = QLineEdit(formWidget)
        formLayout.setWidget(2, QFormLayout.FieldRole, self.userField)
        self.passField = QLineEdit(formWidget)
        self.passField.setEchoMode(QLineEdit.Password)
        formLayout.setWidget(3, QFormLayout.FieldRole, self.passField)
        self.portField = QLineEdit(formWidget)
        formLayout.setWidget(4, QFormLayout.FieldRole, self.portField)

        if 'groupname' in fieldValue:
            self.groupField.setCurrentIndex(self.groupField.findData(fieldValue['groupname'], Qt.DisplayRole))
        if 'hostname' in fieldValue:
            self.hostField.setText(fieldValue['hostname'])
        if 'username' in fieldValue:
            self.userField.setText(fieldValue['username'])
        if 'password' in fieldValue:
            self.passField.setText(fieldValue['password'])
        if 'port' in fieldValue:
            self.portField.setText(fieldValue['port'])

        addButton = QPushButton(formWidget)
        addButton.setText('Save Server')
        formLayout.setWidget(5, QFormLayout.FieldRole, addButton)

        addButton.clicked.connect(self.saveServer)

        self.serverDialog.exec_()

    def saveServer(self):

        if isinstance(self.groupField, QComboBox):
            groupname = self.groupField.currentText()
        if isinstance(self.groupField, QLineEdit):
            groupname = self.groupField.text()

        newServerData = {
            'groupname':groupname,
            'hostname':self.hostField.text(),
            'username':self.userField.text(),
            'password':self.passField.text(),
            'port':self.portField.text()
         }

        self.serverModel.insertServer(newServerData)
        self.listServer()
        self.serverDialog.close()

    def removeServer(self):

        hostname = self.currentData()['hostname']
        reply = QMessageBox.question(self.MainWindow, 'Message', "Are you sure wanna delete the server " + hostname + " ?", QMessageBox.Yes, QMessageBox.Close)

        if reply == QMessageBox.Yes:
            self.serverModel.deleteServer(hostname)
            self.listServer()