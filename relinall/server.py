from relinall.window import *

class Server(Window):

    def __init__(self):
        super().__init__()
        print("server")

        self.serverTreeView()
        self.listServer()

    def serverTreeView(self):
        self.serverTree = QTreeView(self.centralwidget)
        self.serverTree.setMaximumSize(QSize(200, 16777215))
        self.serverTree.setObjectName("serverTree")
        self.serverTree.setSortingEnabled(True)
        self.serverTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.serverTree.setExpandsOnDoubleClick(True)
        self.serverTree.setAnimated(True)
        self.serverTree.setWordWrap(True)
        self.serverTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.serverTree.customContextMenuRequested.connect(self.openMenu)
        self.gridLayout.addWidget(self.serverTree, 1, 0, 1, 1)

    def openMenu(self, position):
    
        indexes = self.serverTree.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        self.menu = QMenu()
        if level == 0:
            self.menu.addAction("Add Server", self.addServer)

        elif level == 1:
            self.menu.addAction("Edit Server", self.editServer)
            self.menu.addAction("Remove Server", self.removeServer)
            self.menu.addSeparator()
            self.menu.addAction("Summary", self.summary)
            self.menu.addAction("Putty", self.putty)
            self.menu.addAction("Services", self.service)
        
        self.menu.exec_(self.serverTree.viewport().mapToGlobal(position))

    def serverDock(self):

        currentData = self.currentData()

        if currentData['hostname'] not in self.serverWidget:
            dockWidget = QDockWidget( currentData['hostname'] + ' (' + currentData['groupname'] +')')
            dockWidget.setMinimumWidth(700)
            dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
            
            self.MainWindow.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

            if self.prevDockWidget:
                self.MainWindow.tabifyDockWidget(self.prevDockWidget, dockWidget)
            else:
                self.prevDockWidget = dockWidget

            # dock.visibilityChanged.connect(self.tt)
            tabWidget = QTabWidget(self.centralwidget)
            tabWidget.setObjectName("tabWidget")
            tabWidget.setTabsClosable(True)
            tabWidget.tabCloseRequested.connect(self.featureTabClose)

            dockWidget.setWidget(tabWidget)

            self.serverWidget[currentData['hostname']] = {}
            self.serverWidget[currentData['hostname']]['dock'] = dockWidget
            self.serverWidget[currentData['hostname']]['tab'] = tabWidget
            
        else:
            dockWidget = self.serverWidget[currentData['hostname']]['dock']

        dockWidget.setVisible(True)
        dockWidget.setFocus()
        dockWidget.raise_()
        dockWidget.show()

        return dockWidget

    def featureTab(self, name):

        currentData = self.currentData()
        tabWidget = self.serverWidget[currentData['hostname']]['tab']

        if name not in self.serverWidget[currentData['hostname']]:

            tab = QWidget()
            tabWidget.addTab(tab, name.title())

            self.serverWidget[currentData['hostname']][name] = tab
        else:

            tab = self.serverWidget[currentData['hostname']][name]

        tabWidget.setCurrentWidget(tab)
        tab.show()

    def featureTabClose(self, i):
        currentData = self.currentData()
        tabWidget = self.serverWidget[currentData['hostname']]['tab']
        tabWidget.removeTab(i)

    def listServer(self):
        self.serverData = QStandardItemModel()
        self.serverData.setHorizontalHeaderLabels(["Server List"])
        self.serverTree.setModel(self.serverData)
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
    
    def editServer(self):
        print("edit server")

    def removeServer(self):
        print("remove server")
