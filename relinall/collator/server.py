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

        # Label
        groupLabel = QLabel(formWidget)
        groupLabel.setText('Group Name *')
        formLayout.setWidget(0, QFormLayout.LabelRole, groupLabel)
        hostLabel = QLabel(formWidget)
        hostLabel.setText('Hostname / IP *')
        formLayout.setWidget(1, QFormLayout.LabelRole, hostLabel)
        userLabel = QLabel(formWidget)
        userLabel.setText('Username *')
        formLayout.setWidget(2, QFormLayout.LabelRole, userLabel)
        passLabel = QLabel(formWidget)
        passLabel.setText('Password *')
        formLayout.setWidget(3, QFormLayout.LabelRole, passLabel)
        portLabel = QLabel(formWidget)
        portLabel.setText('Port Number \n [0-65535]')
        formLayout.setWidget(4, QFormLayout.LabelRole, portLabel)

        # Fields
        if 'groupname' in fieldValue:
            self.groupnameField = QComboBox(formWidget)
            formLayout.setWidget(0, QFormLayout.FieldRole, self.groupnameField)
            self.groupnameField.setModel(self.serverData)
        else:
            self.groupnameField = QLineEdit(formWidget)
            formLayout.setWidget(0, QFormLayout.FieldRole, self.groupnameField)

        self.hostnameField = QLineEdit(formWidget)
        formLayout.setWidget(1, QFormLayout.FieldRole, self.hostnameField)
        self.usernameField = QLineEdit(formWidget)
        formLayout.setWidget(2, QFormLayout.FieldRole, self.usernameField)
        self.passwordField = QLineEdit(formWidget)
        self.passwordField.setEchoMode(QLineEdit.Password)
        formLayout.setWidget(3, QFormLayout.FieldRole, self.passwordField)
        self.portField = QLineEdit(formWidget)
        self.portField.setText('22')
        formLayout.setWidget(4, QFormLayout.FieldRole, self.portField)

        # Validator
        if 'groupname' not in fieldValue:
            groupnameExp = QRegExp(".{2,30}")
            groupnameValidator = QRegExpValidator(groupnameExp, self.groupnameField)
            self.groupnameField.setValidator(groupnameValidator)
            self.groupnameField.textChanged.connect(self.validateServerFormOnChange)
            self.groupnameField.textChanged.emit(self.groupnameField.text())

        # hostnameExp = QRegExp(".{1,50}")
        hostnameExp = QRegExp(self.domainOrIpRegex())
        hostnameValidator = QRegExpValidator(hostnameExp, self.hostnameField)
        self.hostnameField.setValidator(hostnameValidator)
        self.hostnameField.textChanged.connect(self.validateServerFormOnChange)
        self.hostnameField.textChanged.emit(self.hostnameField.text())
        usernameExp = QRegExp(".{1,30}")
        usernameValidator = QRegExpValidator(usernameExp, self.usernameField)
        self.usernameField.setValidator(usernameValidator)
        self.usernameField.textChanged.connect(self.validateServerFormOnChange)
        self.usernameField.textChanged.emit(self.usernameField.text())
        passwordExp = QRegExp(".{1,30}")
        passwordValidator = QRegExpValidator(passwordExp, self.passwordField)
        self.passwordField.setValidator(passwordValidator)
        self.passwordField.textChanged.connect(self.validateServerFormOnChange)
        self.passwordField.textChanged.emit(self.passwordField.text())
        portExp = QRegExp(self.portRegex())
        portValidator = QRegExpValidator(portExp, self.portField)
        self.portField.setValidator(portValidator)
        self.portField.textChanged.connect(self.validateServerFormOnChange)
        self.portField.textChanged.emit(self.portField.text())


        if 'groupname' in fieldValue:
            self.groupnameField.setCurrentIndex(self.groupnameField.findData(fieldValue['groupname'], Qt.DisplayRole))
        if 'hostname' in fieldValue:
            self.hostnameField.setText(fieldValue['hostname'])
        if 'username' in fieldValue:
            self.usernameField.setText(fieldValue['username'])
        if 'password' in fieldValue:
            self.passwordField.setText(fieldValue['password'])
        if 'port' in fieldValue:
            self.portField.setText(fieldValue['port'])

        addButton = QPushButton(formWidget)
        addButton.setText('Save Server')
        formLayout.setWidget(5, QFormLayout.FieldRole, addButton)

        addButton.clicked.connect(self.saveServer)

        self.serverDialog.exec_()

    def saveServer(self):

        if isinstance(self.groupnameField, QComboBox):
            groupname = self.groupnameField.currentText()
        if isinstance(self.groupnameField, QLineEdit):
            groupname = self.groupnameField.text()

        newServerData = {
            'groupname':groupname,
            'hostname':self.hostnameField.text(),
            'username':self.usernameField.text(),
            'password':self.passwordField.text(),
            'port':self.portField.text()
         }

        if not self.validateServerFormOnSubmit(newServerData):
            reply = None
            ssh, error = Ssh.connect(newServerData['hostname'], newServerData['username'], newServerData['password'], newServerData['port'])

            if error:
                reply = QMessageBox.question(self.MainWindow, 'Message', "Failed to connect the server <b>" + newServerData['hostname'] + "</b>, Still wanna save the server details?", QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes or not error:
                self.serverModel.insertServer(newServerData)                
                self.listServer()
                modelIndex = self.serverData.findItems(newServerData['groupname'])[0].index()
                self.treeView.expand(modelIndex)

                self.serverDialog.close()
                QMessageBox.information(self.MainWindow, 'Warning', "Server details has been saved successfully", QMessageBox.Ok)
    
    def removeServer(self):

        hostname = self.currentData()['hostname']
        reply = QMessageBox.question(self.MainWindow, 'Message', "Are you sure wanna delete the server " + hostname + " ?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.serverModel.deleteServer(hostname)
            self.listServer()

    def domainOrIpRegex(self):

        ip = "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
        domain = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"

        return ip

    def portRegex(self):

        return "([0-9]{0,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"

    def validateServerFormOnSubmit(self, fields):

        states = []

        for field in fields:
            fieldObj = getattr(self, field + "Field")
            if isinstance(fieldObj, QLineEdit):
                
                state = fieldObj.validator().validate(fieldObj.text(),0)[0]

                if state == QValidator.Acceptable:
                    color = '#c4df9b' # green
                elif state == QValidator.Intermediate:
                    states.append(field)
                    color = '#f6989d' # yellow
                else:
                    color = '#f6989d' # red
                    states.append(field)
                fieldObj.setStyleSheet('QLineEdit { background-color: %s }' % color)

        return states

    def validateServerFormOnChange(self, *args, **kwargs):

        sender = self.MainWindow.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b' # green
        elif state == QValidator.Intermediate:
            color = '#ffffff' # yellow
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
