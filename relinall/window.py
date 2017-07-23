from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from relinall.db import *
from relinall.util import *

import sys, json

class Window(object):

    width = 900
    height = 700
    serverSub = None
    prevDockWidget = None
    serverWidget = {}

    def __init__(self):
        self.MainWindow = QMainWindow()

        # Main Window
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(self.width, self.height)
        self.MainWindow.setWindowTitle("ReLinAll")
        self.MainWindow.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)

        self.menuBar()
        self.centralLayout()
        self.gridLayout()
        self.statusBar()
        
        QMetaObject.connectSlotsByName(self.MainWindow)
        self.MainWindow.show()

    def centralLayout(self):
        self.centralwidget = QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.MainWindow.setCentralWidget(self.centralwidget)

    def gridLayout(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout.addLayout(self.gridLayout)

    def menuBar(self):
        self.menubar = QMenuBar(self.MainWindow)
        self.menubar.setObjectName("menubar")

        self.relinallMenu()

        self.MainWindow.setMenuBar(self.menubar)

    def relinallMenu(self):
        self.menuReLinAll = QMenu(self.menubar)
        self.menuReLinAll.setObjectName("menuReLinAll")
        self.menuReLinAll.setTitle("ReLinAll")

        self.aboutMenu()
        self.helpMenu()

        self.menubar.addAction(self.menuReLinAll.menuAction())

    def aboutMenu(self):
        self.actionAbout = QAction(self.MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText( "About")
        self.menuReLinAll.addAction(self.actionAbout)

    def helpMenu(self):
        self.actionHelp = QAction(self.MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionHelp.setText("Help")
        self.menuReLinAll.addAction(self.actionHelp)

    def currentData(self):

        index = self.serverTree.selectedIndexes()[0]
        crawler = index.model().itemFromIndex(index)
        return Util.getData(crawler.data())

    def statusBar(self):
        self.statusbar = QStatusBar(self.MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.MainWindow.setStatusBar(self.statusbar)