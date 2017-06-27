from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from relinall.db import *

import sys

class MainWindow(object):

    width = 900
    height = 700
    serverSub = None

    def __init__(self):
        app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.setupUi()
        self.MainWindow.show()
        sys.exit(app.exec_())

    def setupUi(self):

        # Main Window
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(self.width, self.height)
        self.MainWindow.setWindowTitle("ReLinAll")

        self.centralLayout()

        self.statusBar()
        
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def centralLayout(self):
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.gridLayout()
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.serverList()

    def gridLayout(self):
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.menuBar()

        self.serverTreeView()
        # self.mainTabWidget()

        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.gridLayout.addWidget(self.mdiArea, 1, 1, 1, 1)

        self.horizontalLayout.addLayout(self.gridLayout)

    def menuBar(self):
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")

        self.relinallMenu()

        self.MainWindow.setMenuBar(self.menubar)

    def relinallMenu(self):
        self.menuReLinAll = QtWidgets.QMenu(self.menubar)
        self.menuReLinAll.setObjectName("menuReLinAll")
        self.menuReLinAll.setTitle("ReLinAll")

        self.aboutMenu()
        self.helpMenu()

        self.menubar.addAction(self.menuReLinAll.menuAction())

    def aboutMenu(self):
        self.actionAbout = QtWidgets.QAction(self.MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText( "About")
        self.menuReLinAll.addAction(self.actionAbout)

    def helpMenu(self):
        self.actionHelp = QtWidgets.QAction(self.MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setText("Help")
        self.menuReLinAll.addAction(self.actionHelp)

    def serverTreeView(self):
        self.serverTree = QtWidgets.QTreeView(self.centralwidget)
        self.serverTree.setMaximumSize(QtCore.QSize(200, 16777215))
        self.serverTree.setObjectName("serverTree")
        self.serverTree.setSortingEnabled(True)
        # self.serverTree.setHeaderHidden(True)
        self.serverTree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.serverTree.setExpandsOnDoubleClick(True)
        self.serverTree.setAnimated(True)
        self.serverTree.setWordWrap(True)
        self.serverTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.serverTree.customContextMenuRequested.connect(self.openMenu)
        # serverTreeHeader = QtWidgets.QHeaderView(Qt.Horizontal,self.centralwidget)
        # serverTreeHeader.setText("Servers")
        # self.serverTree.setHeader(serverTreeHeader)
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
            self.menu.addAction("Summary", self.removeServer)
            self.menu.addAction("Putty", self.removeServer)
            self.menu.addAction("Services", self.removeServer)
        
        self.menu.exec_(self.serverTree.viewport().mapToGlobal(position))

    def addServer(self):

        # if self.serverSub is None:
        self.serverSub = QMdiSubWindow()
        self.mdiArea.addSubWindow(self.serverSub)

        index = self.serverTree.selectedIndexes()[0]
        crawler = index.model().itemFromIndex(index)

        print(crawler.text())
        self.serverSub.show()
        self.serverSub.activateWindow()
        self.serverSub.showMaximized()
        self.serverSub.setWindowTitle(crawler.text())

    def editServer(self):
        print("edit")

    def removeServer(self):
        print("remove")

    def serverList(self):
        self.serverData = QStandardItemModel()
        self.serverTree.setModel(self.serverData)
        s = server()
        data = s.getServerGrouped()
        
        # for file in data:
        #     item = QStandardItem(file[1])
        #     self.serverData.appendRow(item)
        for group in data:
            serverGroup = QStandardItem(group + "(" + str(data[group]['count']) + ")")
            for host in data[group]['list']:
                serverDetails = QStandardItem(host['hostname'])
                serverGroup.appendRow(serverDetails)
            self.serverData.appendRow(serverGroup)
                

    def mainTabWidget(self):
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.summaryTabView()
        self.puttyTabView()

        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)
        # self.tabWidget.setCurrentIndex(0)

    def summaryTabView(self):
        self.summaryTab = QtWidgets.QWidget()
        self.summaryTab.setObjectName("summaryTab")
        self.tabWidget.addTab(self.summaryTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.summaryTab),  "Summary")

    def puttyTabView(self):
        self.puttyTab = QtWidgets.QWidget()
        self.puttyTab.setObjectName("puttyTab")
        self.tabWidget.addTab(self.puttyTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.puttyTab), "Putty")

    def statusBar(self):
        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)

# class Server():



data = [
    ("Alice", [
        ("Keys", []),
        ("Purse", [
            ("Cellphone", [])
            ])
        ]),
    ("Bob", [
        ("Wallet", [
            ("Credit card", []),
            ("Money", [])
            ])
        ])
    ]

class Window(QWidget):

    def __init__(self):
   
        QWidget.__init__(self)
        
        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        
        self.model = QStandardItemModel()
        self.addItems(self.model, data)
        self.treeView.setModel(self.model)
        
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
        
        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
    
    def addItems(self, parent, elements):
    
        for text, children in elements:
            item = QStandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItems(item, children)
    
    def openMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        
        menu.exec_(self.treeView.viewport().mapToGlobal(position))


class PuttyTab(MainWindow):

    def __init__(self):

        self.serialPort = QtWidgets.QSerialPort(self.puttyTab)