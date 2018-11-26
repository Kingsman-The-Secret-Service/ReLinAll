from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from relinall.util.db import *
from relinall.util.helper import *
from relinall.util.ssh import *
from jinja2 import *

import sys, os

class Window(object):

    width = 900
    height = 700
    prevDockWidget = None
    widgetData = {}

    def __init__(self):

        self.MainWindow = QMainWindow()

        # Main Window
        self.MainWindow.resize(self.width, self.height)
        self.MainWindow.setWindowTitle("ReLinAll")
        self.MainWindow.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)
        # self.MainWindow.showMaximized()

        self.menuBar()
        self.treeView()
        self.statusBar()
        
        QMetaObject.connectSlotsByName(self.MainWindow)
        self.MainWindow.show()

    def menuBar(self):
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setObjectName("menubar")
        self.serverMenu()
        self.relinallMenu()
        self.MainWindow.setMenuBar(self.menubar)

    def relinallMenu(self):
        menuReLinAll = QMenu(self.menubar)
        menuReLinAll.setTitle("ReLinAll")
        menuReLinAll.addAction("About", self.aboutMenu)
        menuReLinAll.addAction("Help", self.helpMenu)
        self.menubar.addAction(menuReLinAll.menuAction())

    def aboutMenu(self):
        print("About")

    def helpMenu(self):
        print("Help")

    def serverMenu(self):
        menuServer = QMenu(self.menubar)
        menuServer.setTitle("Server")
        menuServer.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
        self.menubar.addAction(menuServer.menuAction())

    def treeView(self):
        dockWidget = QDockWidget()
        dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.treeView = QTreeView()
        self.treeView.setMaximumSize(QSize(200, 16777215))
        self.treeView.setGeometry(QRect(10, 10, 200, self.height))
        self.treeView.setObjectName("treeView")
        self.treeView.setSortingEnabled(True)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setExpandsOnDoubleClick(True)
        self.treeView.setAnimated(True)
        self.treeView.setWordWrap(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.treeContextMenu)

        dockWidget.setWidget(self.treeView)

        self.MainWindow.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

    def treeContextMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()

        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QMenu()
        if level == 0:
            menu.addAction("Add Server", self.addServer).setObjectName('ContextAddServer')
            menu.addSeparator()
            menu.addAction("Remove Group", self.removeGroup).setObjectName('ContextAddServer')

        elif level == 1:
            menu.addAction("Summary", self.summary)
            menu.addAction("Ftp", self.ftp)
            # menu.addAction("Putty", self.putty)
            # menu.addAction("Services", self.service)
            
            menu.addSeparator()
            menu.addAction("Edit Server", self.editServer)
            menu.addAction("Remove Server", self.removeServer)
        
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def docker(self, tabName):

        currentData = self.currentData()

        self.statusbar.showMessage("Connecting to " + currentData['hostname'])
        ssh, error = Ssh.connect(currentData['hostname'], currentData['username'], currentData['password'], currentData['port'])

        if error:
            self.statusbar.showMessage("Failed to connect " + currentData['hostname'])
        else:

            if currentData['hostname'] not in self.widgetData:
                dockWidget = QDockWidget( currentData['hostname'] + ' (' + currentData['groupname'] +')')
                dockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
                
                self.MainWindow.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

                if self.prevDockWidget:
                    self.MainWindow.tabifyDockWidget(self.prevDockWidget, dockWidget)
                else:
                    self.prevDockWidget = dockWidget

                tabWidget = QTabWidget()
                tabWidget.setObjectName("tabWidget")
                tabWidget.setTabsClosable(True)
                tabWidget.tabCloseRequested.connect(self.tabberClose)

                dockWidget.setWidget(tabWidget)

                self.widgetData[currentData['hostname']] = {}
                self.widgetData[currentData['hostname']]['dock'] = dockWidget
                self.widgetData[currentData['hostname']]['tab'] = tabWidget
                self.widgetData[currentData['hostname']]['ssh'] = ssh
                self.statusbar.showMessage("Connected to " + currentData['hostname'])
            else:
                dockWidget = self.widgetData[currentData['hostname']]['dock']

            dockWidget.setVisible(True)
            dockWidget.setFocus()
            dockWidget.raise_()
            dockWidget.show()

            self.tabber(tabName)

    def tabber(self, name):

        currentData = self.currentData()
        tabWidget = self.widgetData[currentData['hostname']]['tab']

        if name not in self.widgetData[currentData['hostname']]:

            tab = QWidget()
            tabWidget.addTab(tab, name.title())

            self.widgetData[currentData['hostname']][name] = tab
        else:

            tab = self.widgetData[currentData['hostname']][name]
            tabWidget.addTab(tab, name.title())

        tabWidget.setCurrentWidget(tab)
        tab.show()

    def tabberClose(self, i):
        pos = QCursor.pos()
        widgets = qApp.widgetAt(pos)
        widgets.parentWidget().parentWidget().removeTab(i)
    
    def currentData(self):
        try:
            index = self.treeView.selectedIndexes()[0]
        except Exception:
            return {}

        crawler = index.model().itemFromIndex(index)
        return Helper.getData(crawler.data())

    def statusBar(self):
        self.statusbar = QStatusBar(self.MainWindow)
        self.MainWindow.setStatusBar(self.statusbar)

    def render(self, fileName, data):

        currentDirectoryPath = os.path.dirname(os.path.realpath(__file__))
        templatePath = currentDirectoryPath + '/templates/'
        staticPath = 'file://' + currentDirectoryPath + '/static/'
        
        env = Environment(
            loader = FileSystemLoader(templatePath)
        )

        template = env.get_template(fileName)
        html = template.render(data, staticPath = staticPath)
        return html
