#!/usr/bin/python
import os
import sqlite3
from configparser import ConfigParser
import re
from time import strftime

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime
import js8callAPIsupport

serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""


class Ui_FormCheckin(object):
    def setupUi(self, FormCheckin):
        self.MainWindow = FormCheckin
        FormCheckin.setObjectName("FormCheckin")
        FormCheckin.resize(835, 215)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormCheckin.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormCheckin.setWindowIcon(icon)
        self.lineEdit_2 = QtWidgets.QLineEdit(FormCheckin)
        self.lineEdit_2.setGeometry(QtCore.QRect(171, 126, 481, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(67)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(FormCheckin)
        self.label.setGeometry(QtCore.QRect(75, 15, 626, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FormCheckin)
        self.label_2.setGeometry(QtCore.QRect(90, 125, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(FormCheckin)
        self.pushButton.setGeometry(QtCore.QRect(541, 176, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(FormCheckin)
        self.pushButton_2.setGeometry(QtCore.QRect(641, 176, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(FormCheckin)
        QtCore.QMetaObject.connectSlotsByName(FormCheckin)

        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.MainWindow.close)
        self.pushButton.clicked.connect(self.transmit)

        self.MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )




    def retranslateUi(self, FormCheckin):
        _translate = QtCore.QCoreApplication.translate
        FormCheckin.setWindowTitle(_translate("FormCheckin", "CommStat NET Check In"))
        self.lineEdit_2.setText(_translate("FormCheckin", "NTR"))
        self.label.setText(_translate("FormCheckin", "<html><head/><body><p>This check in form is for scheduled nets and will send a special check in </p><p>that will automatically add your check in with callsign and timestamp to the NCS NET Roster.</p><p>The NCS will periodically send an ACK message to the group with the list of checked in stations.   </p><p><br/></p></body></html>"))
        self.label_2.setText(_translate("FormCheckin", "Your Traffic : "))
        self.pushButton.setText(_translate("FormCheckin", "Transmit"))
        self.pushButton_2.setText(_translate("FormCheckin", "Cancel"))


    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
        global state
        if os.path.exists("config.ini"):
            config_object = ConfigParser()
            config_object.read("config.ini")
            userinfo = config_object["USERINFO"]
            systeminfo = config_object["DIRECTEDCONFIG"]
            callsign = format(userinfo["callsign"])
            callsignSuffix = format(userinfo["callsignsuffix"])
            group1 = format(userinfo["group1"])
            group2 = format(userinfo["group2"])
            grid = format(userinfo["grid"])
            path = format(systeminfo["path"])
            serverip = format(systeminfo["server"])
            serverport = format(systeminfo["port"])
            state = format(systeminfo["state"])
            selectedgroup = format(userinfo["selectedgroup"])






    def transmit(self):
        global selectedgroup
        global callsign
        global state

        comments1 = format(self.lineEdit_2.text())
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 3 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Traffic text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox

            return
        group = "@"+selectedgroup

        message = ""+group + " ," + comments + ","+state+","+grid+",{~%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        #res = QMessageBox.question(FormCheckin, "Question", "Are you sure?", QMessageBox.Yes | QMessageBox.No)
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX TX")
        msg.setText("CommStatX will transmit : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()



        self.sendMessage(messageType, messageString)

        self.closeapp()

    def closeapp(self):
        self.MainWindow.close()

    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormCheckin = QtWidgets.QWidget()
    ui = Ui_FormCheckin()
    ui.setupUi(FormCheckin)
    FormCheckin.show()
    sys.exit(app.exec_())
