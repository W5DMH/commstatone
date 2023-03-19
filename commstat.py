import subprocess
import sys
import webbrowser
from random import randint
import feedparser
from file_read_backwards import FileReadBackwards
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QPlainTextEdit, QWidget, QTableWidget, QMenu, \
    QAction, qApp, QScrollArea, QLabel, QDialog, QInputDialog
from PyQt5.QtCore import QUrl, QTime, QTimer, QDateTime, Qt, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
import io
import folium
import sqlite3
import os

import filter
import settings
from settings import Ui_FormSettings
from configparser import ConfigParser
import threading
from subprocess import call
import time
from js8mail import Ui_FormJS8Mail
from js8sms import Ui_FormJS8SMS
from statrep import Ui_FormStatRep
from bulletin import Ui_FormBull
from marquee import Ui_FormMarquee
from checkin import Ui_FormCheckin
from filter import Ui_FilterForm
from members import Ui_FormMembers
from heardlist import Ui_FormHeard
#from roster import Ui_FormRoster
from statack import Ui_FormStatack
#from datareset import Ui_FormReset
from about import Ui_FormAbout
#from addcall import Ui_FormAddCall
import platform
import maidenhead as mh


callsign = ""
callsignSuffix = ""
group1 = ""
group2 = ""
grid = ""
path = ""
selectedgroup = ""
counter = 0
directedcounter = 0
statreprwcnt = 0
bulletinrwcnt = 0
marqueerwcnt = 0
heardrwcnt = 0
dbcounter = 0
mapper = ""
directedsize = 0
data = ""
map_flag = 0
OS = ""
bull1 = 1
bull2 = 3
OS_Directed = ""

statelist = ['AP', 'AO', 'AO', 'BO', 'CN', 'CM', 'CO', 'DN', 'DM', 'DL', 'DO', 'EN', 'EM','EL','EO','FN','FM','FO']
start = '2023-01-01 05:00'
end = '2030-02-23 00:56'
green = True
yellow = True
red = True
grids = statelist
loadflag = 0




class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        global marqueecolor
        global bull1
        global bull2
        global green
        global yellow
        global red
        global start
        global end
        global grids

        self.oscheck()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(400, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)

        self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                   "color: rgb(0, 200, 0);")

        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0,0, 1, 3, QtCore.Qt.AlignCenter)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                   "color: rgb(0, 200, 0);")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_3.setText("Current Group : AMMRRON")


        self.readconfig()

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 4)
        #self.loadData()

        if "1" in green:
            greenstat = "ON"
        else:
            greenstat = "OFF"
        if "2" in yellow:
            yellowstat = "ON"
        else:
            yellowstat = "OFF"
        if "3" in red:
            redstat = "ON"
        else:
            redstat = "OFF"



        self.label_start = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        self.label_start.setFont(font)
        self.label_start.setObjectName("label_start")
        self.gridLayout_2.addWidget(self.label_start, 2, 0, 1, 1)
        self.label_start.setText("Filters : Start : "+start+"  |  End : "+end+"| Green : "+greenstat+" |  Yellow : "+yellowstat+" |")

        self.label_filters = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(False)
        self.label_filters.setFont(font)
        self.label_filters.setObjectName("label_start")
        self.gridLayout_2.addWidget(self.label_filters, 2, 1, 1, 3)
        self.label_filters.setText(" Red : "+redstat+" |  Grids : "+grids)

        #self.filtersTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        #self.filtersTextEdit.setObjectName("filtersTextEdit")
        #self.gridLayout_2.addWidget(self.filtersTextEdit, 2, 0, 1, 4)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(font)
        self.gridLayout_2.addWidget(self.plainTextEdit, 3, 0, 1, 4)


        


        #self.widget = QtWidgets.QWidget(self.centralwidget)
        #self.setObjectName("widget")
        #self.gridLayout_2.addWidget(self.widget, 3, 0, 1, 1)
        #self.mapperWidget()
        #mapper.setHtml(data.getvalue().decode())
        #self.gridLayout_2.addWidget(mapper, 3, 0, 1, 1)
        

        
        
        self.widget = QWebEngineView(self.centralwidget)
        self.setObjectName("widget")
        self.gridLayout_2.addWidget(self.widget, 4, 0, 1, 1)
        
        #print("Mapping completed")


        #Bulletins Widget
        self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        #self.gridLayout_2.addWidget(self.tableWidget_2, 3, 1, 1, 3)
        self.gridLayout_2.addWidget(self.tableWidget_2, 4, 1, 1, 3)
        
        #self.loadbulletins()

        self.gridLayout_2.setRowStretch(0, 0);
        self.gridLayout_2.setRowStretch(1, 1);
        #self.gridLayout_2.setRowStretch(2, 1);
        #self.gridLayout_2.setRowStretch(3, 1);
        self.gridLayout_2.setRowStretch(4, 1);
        #self.gridLayout.setRowStretch(0, 3);
        #self.gridLayout.setRowStretch(1, 1);
        #self.gridLayout.setRowStretch(2, 2);
        #self.gridLayout_2.setColumnStretch(0, 1)
        #self.gridLayout_2.setColumnStretch(1, 1)
        #self.gridLayout_2.setColumnStretch(3,1)
        #self.gridLayout_2.setColumnStretch(4,1)

        #self.actionExit_2 = QAction('&actionEXIT', MainWindow)
        #self.actionExit_2.setShortcut('Ctrl+Q')
        #self.actionExit_2.setStatusTip('APPLICATION EXIT')


        #self.actionYellow.triggered.connect(lambda: self.change("yellow"))



        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 886, 22))
        self.menubar.setObjectName("menubar")
        self.menuEXIT = QtWidgets.QMenu(self.menubar)
        self.menuEXIT.setObjectName("menuEXIT")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionJS8EMAIL = QtWidgets.QAction(MainWindow)
        self.actionJS8EMAIL.setObjectName("actionJS8EMAIL")
        self.actionJS8SMS = QtWidgets.QAction(MainWindow)
        self.actionJS8SMS.setObjectName("actionJS8SMS")
        self.actionSTATREP = QtWidgets.QAction(MainWindow)
        self.actionSTATREP.setObjectName("actionSTATREP")

        self.actionNET_CHECK_IN = QtWidgets.QAction(MainWindow)
        self.actionNET_CHECK_IN.setObjectName("actionNET_CHECK_IN")

        self.actionFilter = QtWidgets.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")

        self.actionData = QtWidgets.QAction(MainWindow)
        self.actionData.setObjectName("actionData")

        self.actionMEMBER_LIST = QtWidgets.QAction(MainWindow)
        self.actionMEMBER_LIST.setObjectName("actionMEMBER_LIST")

        #self.actionHEARD_LIST = QtWidgets.QAction(MainWindow)
        #self.actionHEARD_LIST.setObjectName("actionHEARD_LIST")

        self.actionSTATREP_ACK = QtWidgets.QAction(MainWindow)
        self.actionSTATREP_ACK.setObjectName("actionSTATREP_ACK")
        self.actionNET_ROSTER = QtWidgets.QAction(MainWindow)
        self.actionNET_ROSTER.setObjectName("actionNET_ROSTER")
        self.actionNEW_MARQUEE = QtWidgets.QAction(MainWindow)
        self.actionNEW_MARQUEE.setObjectName("actionNEW_MARQUEE")
        self.actionFLASH_BULLETIN = QtWidgets.QAction(MainWindow)
        self.actionFLASH_BULLETIN.setObjectName("actionFLASH_BULLETIN")
        self.actionSETTINGS = QtWidgets.QAction(MainWindow)
        self.actionSETTINGS.setObjectName("actionSETTINGS")
        
        #self.actionADDCALL = QtWidgets.QAction(MainWindow)
        #self.actionADDCALL.setObjectName("actionADDCALL")
        
        
        #self.actionDATA_RESET = QtWidgets.QAction(MainWindow)
        #self.actionDATA_RESET.setObjectName("actionDATA_RESET")
        self.actionHELP = QtWidgets.QAction(MainWindow)
        self.actionHELP.setObjectName("actionHELP")
        self.actionABOUT = QtWidgets.QAction(MainWindow)
        self.actionABOUT.setObjectName("actionABOUT")

        self.actionEXIT_2 = QtWidgets.QAction(MainWindow)
        self.actionEXIT_2.setObjectName("actionEXIT_2")


        self.menuEXIT.addAction(self.actionJS8EMAIL)
        self.actionJS8EMAIL.triggered.connect(self.js8email_window)
        self.menuEXIT.addAction(self.actionJS8SMS)
        self.actionJS8SMS.triggered.connect(self.js8sms_window)
        self.menuEXIT.addAction(self.actionSTATREP)
        self.actionSTATREP.triggered.connect(self.statrep_window)
        self.menuEXIT.addAction(self.actionNET_CHECK_IN)
        self.actionNET_CHECK_IN.triggered.connect(self.checkin_window)




        self.menuEXIT.addAction(self.actionMEMBER_LIST)
        self.actionMEMBER_LIST.triggered.connect(self.members_window)

        #self.menuEXIT.addAction(self.actionHEARD_LIST)
        #self.actionHEARD_LIST.triggered.connect(self.heard_window)


        self.menuEXIT.addSeparator()
        self.menuEXIT.addAction(self.actionSTATREP_ACK)
        self.actionSTATREP_ACK.triggered.connect(self.statack_window)
        self.menuEXIT.addAction(self.actionNET_ROSTER)
        self.actionNET_ROSTER.triggered.connect(self.thread_netmanage)
        self.menuEXIT.addAction(self.actionNEW_MARQUEE)
        self.actionNEW_MARQUEE.triggered.connect(self.marquee_window)
        self.menuEXIT.addAction(self.actionFLASH_BULLETIN)
        self.actionFLASH_BULLETIN.triggered.connect(self.bull_window)
        self.menuEXIT.addSeparator()

        self.menuEXIT.addAction(self.actionFilter)
        self.actionFilter.triggered.connect(self.filter_window)

        self.menuEXIT.addAction(self.actionData)
        self.actionData.triggered.connect(self.data_window)

        self.menuEXIT.addAction(self.actionSETTINGS)
        self.actionSETTINGS.triggered.connect(self.settings_window)
        
        #self.menuEXIT.addAction(self.actionADDCALL)
        #self.actionADDCALL.triggered.connect(self.addcall_window)


        #self.menuEXIT.addAction(self.actionDATA_RESET)
        #self.actionDATA_RESET.triggered.connect(self.reset_window)
        self.menuEXIT.addAction(self.actionHELP)
        self.actionHELP.triggered.connect(self.open_webbrowser)
        self.menuEXIT.addAction(self.actionABOUT)
        self.actionABOUT.triggered.connect(self.about_window)

        self.menuEXIT.addSeparator()
        self.menuEXIT.addAction(self.actionEXIT_2)
        self.actionEXIT_2.triggered.connect(qApp.quit)
        self.menubar.addAction(self.menuEXIT.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # update every second
        self.showTime()

        self.timeLine = QtCore.QTimeLine()
        self.timeLine.setCurveShape(QtCore.QTimeLine.LinearCurve)                   # linear Timeline
        self.timeLine.frameChanged.connect(self.setText)
        self.timeLine.finished.connect(self.nextNews)
        self.signalMapper = QtCore.QSignalMapper(self)
        
        self.oscheck()

        #time.sleep(1)

        #self.loadbulletins()

        self.feed()
        #self.directed()
        self.filetest()


        finalpath = os.path.normpath(path)
        #print(finalpath)
        #watch = QtCore.QFileSystemWatcher(self)
        #watch.addPath(finalpath)
        #print("this is finalpath"+finalpath)
        #watch.fileChanged.connect(self.thread)
        #print("JS8 file changed")



        finalpath2 = os.path.abspath(os.getcwd())
        finalpath3 = finalpath2+"/copyDIRECTED.TXT"
        #watch2 = QtCore.QFileSystemWatcher(self)
        #watch2.addPath(finalpath3)
        #print("this is finalpath3 "+finalpath3)
        #watch2.fileChanged.connect(self.directed)
        
        #finalpath2 = os.path.abspath(os.getcwd())
        #finalpath4 = finalpath2+"\\traffic.db3"
        #watch3 = QtCore.QFileSystemWatcher(self)
        #watch3.addPath(finalpath4)
        #print(finalpath3)
        #watch3.fileChanged.connect(self.directed)






    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CommStat Ver 1.0.3"))
        self.actionFilter.setText(_translate("MainWindow", "DISPLAY FILTER"))
        self.actionData.setText(_translate("MainWindow", "DATA MANAGER"))
        self.label.setText(_translate("MainWindow", "TextLabel Marquee"))
        self.label_2.setText(_translate("MainWindow", "TextLabel Clock"))
        self.menuEXIT.setTitle(_translate("MainWindow", "MENU"))
        self.actionJS8EMAIL.setText(_translate("MainWindow", "JS8EMAIL"))
        self.actionJS8SMS.setText(_translate("MainWindow", "JS8SMS"))
        self.actionSTATREP.setText(_translate("MainWindow", "STATREP"))
        self.actionNET_CHECK_IN.setText(_translate("MainWindow", "NET CHECK IN"))
        self.actionMEMBER_LIST.setText(_translate("MainWindow", "MEMBER LIST"))

        #self.actionHEARD_LIST.setText(_translate("MainWindow", "HEARD LIST"))

        self.actionSTATREP_ACK.setText(_translate("MainWindow", "STATREP ACK"))
        self.actionNET_ROSTER.setText(_translate("MainWindow", "NET MANAGER"))
        self.actionNEW_MARQUEE.setText(_translate("MainWindow", "NEW MARQUEE"))
        self.actionFLASH_BULLETIN.setText(_translate("MainWindow", "FLASH BULLETIN"))
        self.actionSETTINGS.setText(_translate("MainWindow", "SETTINGS"))
        #self.actionADDCALL.setText(_translate("MainWindow", "ADDCALL"))
        #self.actionDATA_RESET.setText(_translate("MainWindow", "DATA RESET"))
        self.actionABOUT.setText(_translate("MainWindow", "ABOUT"))
        self.actionHELP.setText(_translate("MainWindow", "HELP"))
        self.actionEXIT_2.setText(_translate("MainWindow", "EXIT"))



    def oscheck(self):
        global OS
        global bull1
        global bull2
        global OS_Directed
        pios = "aarch64"
        winos = "Windows"
        linuxos = "Linux"
        if pios in (platform.platform()):
            print("Commstat this is Pi 64bit OS")
            OS = "pi"
            bull1 = 0
            bull2 = 4
        if winos in (platform.platform()):
            print("Commstat this is Windows OS")
            OS_Directed = "\DIRECTED.TXT"
        # sudo apt install ./python-pyqt5.qtwebengine_5.15.2-2_arm64.deb
        if linuxos in (platform.platform()):
            print("Commstat this is Linux OS")
            OS_Directed = "/DIRECTED.TXT"

        else:
            # print("This is not 64bit PiOS")
            # OS = "Mint"
            print("Commstat operating System is :" + platform.platform())
            print("Commstat Python version is :" + platform.python_version())


    def readconfig(self):
        # Read config.ini file
        config_object = ConfigParser()
        config_object.read("config.ini")
        global callsign
        global callsignSuffix
        global group1
        global group2
        global grid
        global path
        global selectedgroup
        global OS_Directed
        global start
        global end
        global green
        global yellow
        global red
        global grids

        # Get the password
        userinfo = config_object["USERINFO"]
        #print("callsign is {}".format(userinfo["callsign"]))
        #print("callsignsuffix is {}".format(userinfo["callsignsuffix"]))
        #print("group1 is {}".format(userinfo["group1"]))
        #print("group2 is {}".format(userinfo["group2"]))
        #print("grid is {}".format(userinfo["grid"]))
        systeminfo = config_object["DIRECTEDCONFIG"]
        filter = config_object["FILTER"]
        #print("file path  is {}".format(systeminfo["path"]))
        callsign = format(userinfo["callsign"])
        callsignSuffix = format(userinfo["callsignsuffix"])
        group1 = format(userinfo["group1"])
        group2 = format(userinfo["group2"])
        grid = format(userinfo["grid"])
        path1 = format(systeminfo["path"])
        path = (path1+""+OS_Directed)
        selectedgroup = format(userinfo["selectedgroup"])
        #print("this is the new path :"+path)
        #print(selectedgroup)
        start = format(filter["start"])
        end = format(filter["end"])
        green = format(filter["green"])
        yellow = format(filter["yellow"])
        red = format(filter["red"])
        grids = format(filter["grids"])





        if (callsign =="NOCALL"):
            self.settings_window()
            
    def filetest(self):
        global path
        global directedsize    # path
        #print("started file test")
        pathlocal = path
        status = os.stat(path)
        statussize = status.st_size
        #print("Here is the current Directed size : "+str(status.st_size))
        #print("Here is the previous Directed size :"+str(directedsize))
        if statussize != directedsize:
            directedsize = statussize
            self.directed()
            QtCore.QTimer.singleShot(3000, self.directed)
            #print("ran second direct") 
            QtCore.QTimer.singleShot(30000, self.filetest)
        else:
            QtCore.QTimer.singleShot(30000, self.filetest)

    def help_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormSettings()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()



    def settings_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormSettings()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()
        
    #def addcall_window(self):
    #    dialog = QtWidgets.QDialog()
    #    dialog.ui = Ui_FormAddCall()
    #    dialog.ui.setupUi(dialog)
    #    dialog.exec_()
    #    #dialog.show()



    def js8email_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormJS8Mail()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def js8sms_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormJS8SMS()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def statrep_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormStatRep()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def bull_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormBull()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def marquee_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormMarquee()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()


    def checkin_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormCheckin()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def filter_window(self):
        #dialog = QtWidgets.QDialog()
        #dialog.ui = Ui_FilterForm()
        #dialog.ui.setupUi(dialog)
        #dialog.exec_()
        #if dialog.exec_() == QtWidgets.QDialog.Accepted:
        #    print("the filter is completed")
        #dialog.window_closed.connect(self.loadData)
        #subprocess.call([sys.executable, "filter.py"])
        result = subprocess.run([sys.executable, "filter.py"])
        print(result)
        self.loadData()
        self.run_mapper()

    def data_window(self):
        #dialog = QtWidgets.QDialog()
        #dialog.ui = Ui_FilterForm()
        #dialog.ui.setupUi(dialog)
        #dialog.exec_()
        #if dialog.exec_() == QtWidgets.QDialog.Accepted:
        #    print("the filter is completed")
        #dialog.window_closed.connect(self.loadData)
        #subprocess.call([sys.executable, "filter.py"])
        result = subprocess.run([sys.executable, "commdata.py"])
        print(result)




    def members_window(self):
        #dialog = QDialog()
        #dialog.ui = Ui_FormMembers()
        #dialog.ui.setupUi(dialog)
        #dialog.exec_()
        #dialog.show()
        #call(["python", "members.py"])
        subprocess.call([sys.executable, "members.py"])

    #def heard_window(self):
        #dialog = QtWidgets.QDialog()
        #dialog.ui = Ui_FormHeard()
        #dialog.ui.setupUi(dialog)
        #dialog.exec_()
        #dialog.show()
        #call(["python", "heardlist.py"])
    #    subprocess.call([sys.executable, "heardlist.py"])

    def roster_window(self):
        #dialog = QtWidgets.QDialog()
        #dialog.ui = Ui_FormRoster()
        #dialog.ui.setupUi(dialog)
        #dialog.exec_()
        #dialog.show()
        call(["python", "roster.py"])


    def netmanager_window(self):
        #call(["python", "netmanager.py"])
        subprocess.call([sys.executable, "netmanager.py"])


    def thread_netmanage(self):
        t5 = threading.Thread(target=self.netmanager_window)
        t5.start()



    def statack_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormStatack()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def reset_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormReset()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def about_window(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_FormAbout()
        dialog.ui.setupUi(dialog)
        dialog.exec_()
        #dialog.show()

    def loadData(self):
        #print("\n load data restarted")
        self.readconfig()
        #self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        #connection = sqlite3.connect('traffic.db3')
        #query = """SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data where groupname = ?"""
        #result = connection.execute(query,(selectedgroup,))

        global statelist
        global start
        global end
        global green
        global yellow
        global red
        global grids
        global selectedgroup
        print (start)
        print(end)
        print("colors :"+red+" "+yellow+" "+green)
        if "1" in green:
            greenstat = "ON"
        else:
            greenstat = "OFF"
        if "2" in yellow:
            yellowstat = "ON"
        else:
            yellowstat = "OFF"
        if "3" in red:
            redstat = "ON"
        else:
            redstat = "OFF"

        self.label_start.setText("Filters : Start : " + start + "  |  End : " + end + "| Green : " + greenstat + " |  Yellow : " + yellowstat + " |")
        self.label_filters.setText(" Red : " + redstat + " |  Grids : " + grids)


        connection = sqlite3.connect('traffic.db3')
        cursor = connection.cursor()

        query = ("SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments "
                 "FROM StatRep_Data WHERE groupname = ? AND (status  = ? OR status = ? OR status = ?) AND datetime BETWEEN ? AND ? AND substr(grid,1,2) IN ({})".format(', '.join('?' for _ in statelist)))
        result = cursor.execute(query, [selectedgroup, green, yellow, red, start, end] +statelist)





        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(18)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                cellval = self.tableWidget.item(row_number, column_number).text()
                if self.tableWidget.item(row_number, column_number).text() == "1":
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(000, 128, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(000, 128, 000))
                if self.tableWidget.item(row_number, column_number).text() == "2":
                    # print("if statement worked"+cellval)
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(255, 255, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(255, 255, 000))
                if self.tableWidget.item(row_number, column_number).text() == "3":
                    # print("if statement worked" + cellval)
                    self.tableWidget.item(row_number, column_number).setBackground(QtGui.QColor(255, 000, 000))
                    self.tableWidget.item(row_number, column_number).setForeground(QtGui.QColor(255, 000, 000))
                # else:
                #   print("if statement failed"+cellval)

        table = self.tableWidget
        table.setHorizontalHeaderLabels(
            str("Date Time UTC ;ID ;Callsign; Grid ; Priority; Stat; Pow; H2O; Med; Com; Trv; Int; Fuel; Food; Cri; Civ; Pol; Remarks").split(
                ";"))
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setVisible(False)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(False)
        # header.horizontalHeaderStretchLastSection = True
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.sortItems(0, QtCore.Qt.DescendingOrder)
        #self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 4)
        #print("loadData completed \n \n")
        #self.filetest()
        connection.close()
        
    


    def directedpi(self):
        global directedcounter
        with open(path) as f, open('output.txt', 'w') as fout:
            fout.writelines(reversed(f.readlines()))
        text = open('output.txt').read()
        text_edit_widget = QPlainTextEdit(text)
        # text_edit_widget.setStyleSheet(
        #     """QPlainTextEdit {background-color: #7E7C7A;
        #                      color: #FCF55F;
        #                     text-decoration: underline;
        #                    font-family: Courier;}""")
        if directedcounter > 1:
            self.plainTextEdit.setPlainText(text)
        else:
            self.plainTextEdit.setPlainText(text)
            #self.gridLayout_2.addWidget(text_edit_widget, 2, 0, 1, 4)
        directedcounter += 1
        print("Directed completed : counter :"+str(directedcounter))

        self.loadbulletins()
        self.loadData()
        #self.mapperWidget()
        self.run_mapper()
        self.thread()
        
        self.label_3.setText(" Active Group : "+selectedgroup)
        #QtCore.QTimer.singleShot(30000, self.directed)
        
    def directed(self):
        global directedcounter
        with open(path) as f, open('output.txt', 'w') as fout:
            fout.writelines(reversed(f.readlines()))
        text = open('output.txt').read()
        text_edit_widget = QPlainTextEdit(text)
        # text_edit_widget.setStyleSheet(
        #     """QPlainTextEdit {background-color: #7E7C7A;
        #                      color: #FCF55F;
        #                     text-decoration: underline;
        #                    font-family: Courier;}""")
        if directedcounter > 1:
            self.plainTextEdit.setPlainText(text)
        else:
            self.plainTextEdit.setPlainText(text)
            #self.gridLayout_2.addWidget(text_edit_widget, 2, 0, 1, 4)
        directedcounter += 1
        print("Directed completed : counter :"+str(directedcounter))

        self.loadbulletins()
        self.loadData()
        #self.mapperWidget()
        self.run_mapper()
        self.thread()
        
        self.label_3.setText(" Active Group : "+selectedgroup)
        #QtCore.QTimer.singleShot(30000, self.directed)





    def mapperWidget(self):
        global mapper
        global data
        global map_flag
        global statelist
        global start
        global end
        global green
        global yellow
        global red
        global grids
        global selectedgroup

        gridlist = []
        radius = 6
        filler = True
        color = green

        mapper = QWebEngineView()
        coordinate = (38.8199286, -90.4782551)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate

        )

        
        
        #self.widget = QWebEngineView(self.centralwidget)
        #self.setObjectName("widget") 
        #self.gridLayout_2.addWidget(self.widget, 3, 0, 1, 1)

        try:
            connection = sqlite3.connect('traffic.db3')
            cursor = connection.cursor()
            # print("Connected to SQLite")
            #started new query here
            query = (
                "SELECT callsign, SRid, status, grid  FROM StatRep_Data WHERE groupname = ? AND (status  = ? OR status = ? OR status = ?) AND datetime BETWEEN ? AND ? AND substr(grid,1,2) IN ({})".format(
                    ', '.join('?' for _ in statelist)))
            cursor = connection.execute(query, [selectedgroup, green, yellow, red, start, end] + statelist)
            #items = cursor.fetchall()


            #query = (
            #    "SELECT callsign, SRid, status FROM StatRep_Data WHERE groupname = ? AND datetime BETWEEN ? AND ?")
            #cursor = connection.execute(query, (selectedgroup, start, end))
            items = cursor.fetchall()

            for item in items:
                call = item[0]
                srid = item[1]
                status = item[2]
                grid = item[3]
                coords = mh.to_location(grid, center=True)
                testlat = float(coords[0])
                testlong = float(coords[1])
                count = gridlist.count(grid)
                #print(call + " before lat  & Long " + str(testlat) + "  " + str(testlong))
                if count > 0:
                    #print("latbefore :"+str(testlat))
                    testlat = testlat + (count * .010)
                    #print("latafter :" + str(testlat))
                    testlong = testlong +(count * .010)
                gridlist.append(grid)
                #print(call+" After lat  & Long "+str(testlat)+"  "+str(testlong))
                testlat = float(testlat)
                testlong = float(testlong)

                #glat = gridLatint
                #glon = gridLongint
                glat = testlat
                glon = testlong

                #ended new query here
                pinstring = ("Callsign :")
                html = '''<HTML> <BODY><p style="color:blue;font-size:14px;">%s %s<br>
                                StatRep ID :
                                %s  
                                </p></BODY></HTML>''' % (pinstring, call, srid,)
                iframe = folium.IFrame(html,
                                       width=160,
                                       height=70)

                popup = folium.Popup(iframe,
                                     min_width=100, max_width=160)
                #print("status :"+status+" yellow: "+yellow+" red : "+red+" green : "+green)
                #print("starting if loop")

                if red == True:
                    red = "3"
                elif red == False:
                    red = 0
                if yellow == True:
                    yellow = "2"
                elif yellow == False:
                    yellow = 0
                if green == True:
                    green = "1"
                elif green == False:
                    green = 0

                if "2" in status and yellow == "2":
                    color = "orange"
                    radius = 40
                    filler = True
                    #print("this is yellow 2 "+yellow)
                elif "2" in status and yellow == "0":
                    color = ""
                    radius = 40
                    filler = False
                    #print("this is NOT yellow 2 " +yellow)

                elif "3" in status and red == "3":
                    color = "red"
                    radius = 40
                    filler = True
                    #print("this is red" +red)
                elif "3" in status and red == "0":
                    color = ""
                    radius = 40
                    filler = False
                    #print("this is NOT red" + red)

                elif "1" in status and green == "1":
                    color = "green"
                    radius = 6
                    filler = True
                    #print("this is green" +green)
                elif "1" in status and green == "0":
                    color = ""
                    radius = 6
                    filler = False
                    #print("this is NOT green" +green)




                #folium.Marker(location=[glat, glon], popup=popup).add_to(m)
                #folium.CircleMarker(radius=6,fill=True, fill_color="darkblue",
                #    location=[glat, glon], popup=popup, icon=folium.Icon(color="red")).add_to(m)
                folium.CircleMarker(radius=radius,fill=filler, color=color, fill_color=color,location=[glat, glon], popup=popup, icon=folium.Icon(color="red")).add_to(m)


            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (connection):
                connection.close()
        #       print("The SQLite connection is closed")
        # return map

        # folium.Marker(location=[38.655800, -87.274721],popup='<h3 style="color:green;">Marker2</h3>').add_to(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        

        #self.gridLayout.addWidget()widget = QWebEngineView()
        if map_flag == 1:
            self.widget.reload()
            print("\n \n executed map reload \n \n")
            
        else:
            self.widget.setHtml(data.getvalue().decode())
            map_flag = 0
            print("\n \n executed map update \n \n")
        #self.widget.update()
        
        
        #self.gridLayout_2.addWidget(mapper, 3, 0, 1, 1)
        #print("Mapping completed")
        #QtCore.QTimer.singleShot(30000, self.widget.deleteLater)
        #QtCore.QTimer.singleShot(30500, self.mapperWidget)
        #QtCore.QTimer.singleShot(30000, self.run_mapper)
    
    
    def run_mapper(self):
        global mapper
        global data
        global os
        if "Pi" in OS:
            #self.mapperWidgetpi()
            print("\n \n OS is Pi map is removed \n \n ")
                  
        else:
            self.mapperWidget()
            print("\n \n OS is not Pi \n \n ") 
        #mapper.deleteLater()
        #self.widget.deleteLater()
        #print("stopped previous map")
        #self.mapperWidget()
        #self.widget.reload()
        #print ("reloaded")
            
    
    def loadbulletins(self):
        self.readconfig()
        #self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
        connection = sqlite3.connect('traffic.db3')
        query = "SELECT datetime, idnum, callsign, message FROM bulletins_Data where groupid = ?"
        result = connection.execute(query, (selectedgroup,))
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(4)
        for row_number, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        table = self.tableWidget_2
        table.setHorizontalHeaderLabels(
            str("Date Time UTC ;ID ;Callsign; Bulletin ;").split(
                ";"))
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.sortItems(0, QtCore.Qt.DescendingOrder)
        #self.gridLayout_2.addWidget(self.tableWidget_2, 3, 1, 1, 3)

        #print("Load Bulletins & Marquee Completed")
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)


        #print("Load Bulletins & Marquee Completed")
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)



    def thread_second():
        call(["python", "datareader.py"])

    #processThread = threading.Thread(target=thread_second)  # <- note extra ','
    #processThread.daemon = True
    #processThread.start()

    def showTime(self):
        #currentTime = QTime.currentTime()
        #currentTime = QTime.toUTC()
        now = QDateTime.currentDateTime()
        displayTxt = (now.toUTC().toString(Qt.ISODate))
        self.label_2.setText(" "+displayTxt+" ")

    def thread(self):
        t1 = threading.Thread(target=self.Operation)
        t1.start()

    def Operation(self):
        global counter
        now = QDateTime.currentDateTime()
        displayTxt = (now.toUTC().toString(Qt.ISODate))
        
        print("Time Datatreader Start :"+displayTxt)
        counter += 1
        print("Thread counter = "+str(counter))
        #call(["python", "datareader.py"])
        subprocess.call([sys.executable, "datareader.py"])

        #time.sleep(10)
        #print("Datareader stopped :"+displayTxt)


    def feed(self):
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)
        marqueegreen = "color: rgb(0, 200, 0);"
        marqueeyellow = "color: rgb(255, 255, 0);"
        marqueered = "color: rgb(255, 0, 0);"
        connection = sqlite3.connect('traffic.db3')
        query = "SELECT* FROM marquees_data WHERE groupname = ? ORDER BY date DESC LIMIT 1"
        result = connection.execute(query, (selectedgroup,))
        result = result.fetchall()
        

        callSend = (result[0][2])
        id = (result[0][1])
        group = (result[0][3])
        date = (result[0][4])
        msg = (result[0][6])
        color = (result[0][5])
        if (color == "2"):
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueered + "")
        elif(color == "1"):
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueeyellow + "")
        else:
            self.label.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "" + marqueegreen + "")

        marqueetext = (" ID "+id+" Received  : "+date+"  From : "+group+" by : "+callSend+" MSG : "+msg )
        connection.close()
        fm = self.label.fontMetrics()
        self.nl = int(self.label.width()/fm.averageCharWidth())     # shown stringlength
        news = [marqueetext]
        appendix = ' '*self.nl                      # add some spaces at the end
        news.append(appendix)
        delimiter = '      +++      '                   # shown between the messages
        self.news = delimiter.join(news)
        newsLength = len(self.news)                 # number of letters in news = frameRange
        lps = 6                                 # letters per second
        dur = newsLength*500/lps               # duration until the whole string is shown in milliseconds
        self.timeLine.setDuration(20000)
        self.timeLine.setFrameRange(0, newsLength)
        self.timeLine.start()


    def setText(self, number_of_frame):
        if number_of_frame < self.nl:
            start = 0
        else:
            start = number_of_frame - self.nl
        text = '{}'.format(self.news[start:number_of_frame])
        self.label.setText(text)
        self.label.setFixedWidth(400)

    def nextNews(self):
        self.feed()                             # start again

    def setTlText(self, text):
        string = '{} pressed'.format(text)
        self.textLabel.setText(string)

    def open_webbrowser(self):
        webbrowser.open('CommStat_Help.pdf')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
