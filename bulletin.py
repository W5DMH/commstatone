# -*- coding: utf-8 -*-

import os
import sqlite3
from configparser import ConfigParser
import re
from time import strftime

from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime


import js8callAPIsupport


serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""
bull_id =""
man_call =""


class Ui_FormBull(object):
    def setupUi(self, FormBull):
        self.MainWindow = FormBull
        FormBull.setObjectName("FormBull")
        FormBull.resize(835, 215)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormBull.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormBull.setWindowIcon(icon)

        self.lineEdit_2 = QtWidgets.QLineEdit(FormBull)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 481, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(67)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(FormBull)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 148, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")


        self.lineEdit_3 = QtWidgets.QLineEdit(FormBull)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 65, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setMaxLength(8)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(FormBull)
        self.label_3.setGeometry(QtCore.QRect(58, 65, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")



        self.pushButton = QtWidgets.QPushButton(FormBull)
        self.pushButton.setGeometry(QtCore.QRect(530, 150, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")


        self.pushButton_2 = QtWidgets.QPushButton(FormBull)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 150, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(FormBull)
        self.pushButton_3.setGeometry(QtCore.QRect(430, 150, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")


        self.label = QtWidgets.QLabel(FormBull)
        self.label.setGeometry(QtCore.QRect(162, 20, 523, 16))
        self.label.setObjectName("label")
        
        self.find_bull_id()


        self.retranslateUi(FormBull)
        QtCore.QMetaObject.connectSlotsByName(FormBull)

        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.MainWindow.close)
        self.pushButton.clicked.connect(self.transmit)
        self.pushButton_3.clicked.connect(self.save_only)

        self.MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )



    def retranslateUi(self, FormBull):
        _translate = QtCore.QCoreApplication.translate
        FormBull.setWindowTitle(_translate("FormBull", "CommStat Bulletin"))
        self.label_2.setText(_translate("FormBull", "Bulletin to transmit : "))
        self.label_3.setText(_translate("FormBull", "From Callsign : "))
        self.pushButton.setText(_translate("FormBull", "Transmit"))
        self.pushButton_2.setText(_translate("FormBull", "Cancel"))
        self.pushButton_3.setText(_translate("FormBull", "Save Only"))
        self.label.setText(_translate("FormBull", "This will transmit a message to all stations that will pop up for immediate action"))


    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
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
            selectedgroup = format(userinfo["selectedgroup"])
            self.lineEdit_3.setText(callsign)


            randnum = random.randint(100, 999)


    def save_only(self):
        global man_call
        global selectedgroup
        #global callsign

        global bull_id
        call = format(self.lineEdit_3.text())
        call = call.upper()
        comments1 = format(self.lineEdit_2.text())
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Bulletin too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            msg.raise_()
            x = msg.exec_()  # this will show our messagebox
            return
        if len(call) < 4:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Minimum 4 characters required!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(call) > 8:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Minimum 4 characters required!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if not re.match('[AKNW][A-Z]{0,2}[0-9][A-Z]{1,3}', call):
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Does not meet callsign structure!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return


        group = "@"+selectedgroup
        randnum = random.randint(100, 999)
        #idrand = str(randnum)
        idrand = bull_id


        message = ""+group + " MSG ," + idrand + "," + comments + ",{^%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        print("made it this far 2 ")

        msg = QMessageBox()
        msg.setWindowTitle("CommStatX Save Bulletin")
        msg.setText("CommStatX has saved : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()

        #self.sendMessage(messageType, messageString)




        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        #conn.set_trace_callback(print)
        cur.execute("INSERT OR REPLACE INTO bulletins_Data (datetime,groupid,idnum,callsign,message) VALUES(?,?,?,?,?)",(date,selectedgroup,idrand,call,comments))
        conn.commit()


        print(date,selectedgroup,idrand,call,comments)
        cur.close()
        #datafile = open("copyDIRECTED.TXT", "w")
        #datafile.write("blank line \n" )
        #datafile.close()
        self.closeapp()


    def transmit(self):
        global selectedgroup
        global callsign
        global bull_id

        comments1 = format(self.lineEdit_2.text())
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Bulletin too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            msg.raise_()
            x = msg.exec_()  # this will show our messagebox
            return



        group = "@"+selectedgroup
        randnum = random.randint(100, 999)
        #idrand = str(randnum)
        idrand = bull_id


        message = ""+group + " MSG ," + idrand + "," + comments + ",{^%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message


        #msg = QMessageBox()
        #msg.setWindowTitle("CommStatX TX")
        #msg.setText("CommStatX will transmit : " + message)
        #msg.setIcon(QMessageBox.Information)
        #msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        #x = msg.exec_()

        self.sendMessage(messageType, messageString)




        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        #conn.set_trace_callback(print)
        cur.execute("INSERT OR REPLACE INTO bulletins_Data (datetime,groupid,idnum,callsign,message) VALUES(?,?,?,?,?)",(date,selectedgroup,idrand,callsign,comments))
        conn.commit()


        print(date,selectedgroup,idrand,callsign,comments)
        cur.close()
        datafile = open("copyDIRECTED.TXT", "w")
        datafile.write("blank line \n" )
        datafile.close()
        self.closeapp()
        
    def find_bull_id(self):
        global bull_id
        randnum = random.randint(100, 999)
        bull_id = (str(randnum))
        #stat_id = "902"

        try:
            sqliteConnection = sqlite3.connect('traffic.db3')
            cursor = sqliteConnection.cursor()
           # print("Connected to SQLite")
            sqlite_select_query = 'SELECT idnum FROM bulletins_Data;'
            cursor.execute(sqlite_select_query)
            items = cursor.fetchall()

            for item in items:
                idnum = item[0]
                #print(item)
                if bull_id in item:
                    print("Bulletin random number failed, recycling and trying again")
                    cursor.close()
                    self.find_bull_id()



            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
         #       print("The SQLite connection is closed")
    

    def closeapp(self):
        self.MainWindow.close()

    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormBull = QtWidgets.QWidget()
    ui = Ui_FormBull()
    ui.setupUi(FormBull)
    FormBull.show()
    sys.exit(app.exec_())
