
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
marq_id= ""

class Ui_FormMarquee(object):
    def setupUi(self, FormMarquee):
        self.MainWindow = FormMarquee
        FormMarquee.setObjectName("FormMarquee")
        FormMarquee.resize(835, 275)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormMarquee.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormMarquee.setWindowIcon(icon)
        self.lineEdit_2 = QtWidgets.QLineEdit(FormMarquee)
        self.lineEdit_2.setGeometry(QtCore.QRect(171, 156, 481, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(67)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(FormMarquee)
        self.label.setGeometry(QtCore.QRect(15, 55, 146, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")


        self.lineEdit_3 = QtWidgets.QLineEdit(FormMarquee)
        self.lineEdit_3.setGeometry(QtCore.QRect(171, 126, 60, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setMaxLength(8)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(FormMarquee)
        self.label_3.setGeometry(QtCore.QRect(70, 125, 146, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label3")




        self.label_2 = QtWidgets.QLabel(FormMarquee)
        self.label_2.setGeometry(QtCore.QRect(45, 155, 126, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(FormMarquee)
        self.pushButton.setGeometry(QtCore.QRect(541, 220, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(FormMarquee)
        self.pushButton_2.setGeometry(QtCore.QRect(641, 220, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(FormMarquee)
        self.pushButton_3.setGeometry(QtCore.QRect(441, 220, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.radioButton_Green = QtWidgets.QRadioButton(FormMarquee)
        self.radioButton_Green.setGeometry(QtCore.QRect(185, 25, 89, 20))
        self.radioButton_Green.setObjectName("radioButton_Green")
        self.radioButton_Yellow = QtWidgets.QRadioButton(FormMarquee)
        self.radioButton_Yellow.setGeometry(QtCore.QRect(185, 55, 89, 20))
        self.radioButton_Yellow.setObjectName("radioButton_Yellow")
        self.radioButton_Red = QtWidgets.QRadioButton(FormMarquee)
        self.radioButton_Red.setGeometry(QtCore.QRect(185, 85, 89, 20))
        self.radioButton_Red.setObjectName("radioButton_Red")

        self.retranslateUi(FormMarquee)
        QtCore.QMetaObject.connectSlotsByName(FormMarquee)
        
        self.find_marq_id()

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


    def retranslateUi(self, FormMarquee):
        _translate = QtCore.QCoreApplication.translate
        FormMarquee.setWindowTitle(_translate("FormMarquee", "CommStat Marquee"))
        self.label.setText(_translate("FormMarquee", "Select Marquee Color : "))
        self.label_2.setText(_translate("FormMarquee", "Marquee Message : "))
        self.label_3.setText(_translate("FormMarquee", "From Callsign :"))
        self.pushButton.setText(_translate("FormMarquee", "Transmit"))
        self.pushButton_2.setText(_translate("FormMarquee", "Cancel"))
        self.pushButton_3.setText(_translate("FormMarquee", "Save Only"))
        self.radioButton_Green.setText(_translate("FormMarquee", "Green"))
        self.radioButton_Yellow.setText(_translate("FormMarquee", "Yellow"))
        self.radioButton_Red.setText(_translate("FormMarquee", "Red"))


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
        global selectedgroup
        #global callsign

        comments1 = format(self.lineEdit_2.text())
        comments1 = comments1.upper()
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)
        call = format(self.lineEdit_3.text())
        call = call.upper()

        if len(call) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Callsign too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(call) > 8 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Callsign too long")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return


        if not re.match('[AKNW][A-Z]{0,2}[0-9][A-Z]{1,3}', call):
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Callsign entered does not meet callsign structure requirements!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return


        if len(comments) < 12 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Marquee text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if (self.radioButton_Green.isChecked() == True):
            color = "0"
        elif (self.radioButton_Yellow.isChecked() == True):
            color = "1"
        elif (self.radioButton_Red.isChecked() == True):
            color = "2"
        else:
                msg = QMessageBox()
                msg.setWindowTitle("CommStatX error")
                msg.setText(" Color selection is required!")
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                x = msg.exec_()  # this will show our messagebox
                return


        group = "@"+selectedgroup
        randnum = random.randint(100, 999)
        #idrand = str(randnum)
        idrand = marq_id
        message = ""+ group + " ," + idrand + ","+ color +"," +comments + ",{*%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        ##self.sendMessage(messageType, messageString)
        #msg = QMessageBox()
        #msg.setWindowTitle("CommStatX TX")
        #msg.setText("CommStatX has saved Marquee : " + message)
        #msg.setIcon(QMessageBox.Information)
        #msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        #x = msg.exec_()

        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        conn.set_trace_callback(print)
        cur.execute("INSERT OR REPLACE INTO marquees_Data (idnum,callsign,groupname,date,color, message) VALUES(?,?,?,?,?,?)",(idrand,call, selectedgroup,date,color,comments))
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

        comments1 = format(self.lineEdit_2.text())
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 12 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Marquee text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if (self.radioButton_Green.isChecked() == True):
            color = "0"
        elif (self.radioButton_Yellow.isChecked() == True):
            color = "1"
        elif (self.radioButton_Red.isChecked() == True):
            color = "2"
        else:
                msg = QMessageBox()
                msg.setWindowTitle("CommStatX error")
                msg.setText(" Color selection is required!")
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                x = msg.exec_()  # this will show our messagebox
                return


        group = "@"+selectedgroup
        randnum = random.randint(100, 999)
        #idrand = str(randnum)
        idrand = marq_id
        message = ""+ group + " ," + idrand + ","+ color +"," +comments + ",{*%}"
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        self.sendMessage(messageType, messageString)
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX TX")
        msg.setText("CommStatX will transmit : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()

        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        conn.set_trace_callback(print)
        cur.execute("INSERT OR REPLACE INTO marquees_Data (idnum,callsign,groupname,date,color, message) VALUES(?,?,?,?,?,?)",(idrand,callsign, selectedgroup,date,color,comments))
        conn.commit()


        print(date,selectedgroup,idrand,callsign,comments)
        cur.close()

        datafile = open("copyDIRECTED.TXT", "w")
        datafile.write("blank line \n" )
        datafile.close()



        self.closeapp()
        
    def find_marq_id(self):
        global marq_id
        randnum = random.randint(100, 999)
        marq_id = (str(randnum))
        #stat_id = "902"

        try:
            sqliteConnection = sqlite3.connect('traffic.db3')
            cursor = sqliteConnection.cursor()
           # print("Connected to SQLite")
            sqlite_select_query = 'SELECT idnum FROM marquees_Data ;'
            cursor.execute(sqlite_select_query)
            items = cursor.fetchall()

            for item in items:
                srid = item[0]
                #print(item)
                if marq_id in item:
                    print("Bulletin random number failed, recycling and trying again")
                    cursor.close()
                    self.find_marq_id()



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
    FormMarquee = QtWidgets.QWidget()
    ui = Ui_FormMarquee()
    ui.setupUi(FormMarquee)
    FormMarquee.show()
    sys.exit(app.exec_())
