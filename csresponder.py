
import re
import sys
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDateTime
from PyQt5 import QtCore, QtGui, QtWidgets
import js8callAPIsupport
from configparser import ConfigParser
import os
import sqlite3

serverip = ""
serverport = ""
os.system('')


class Ui_FormJS8Mail(object):
    def setupUi(self, FormJS8Mail):
        self.MainWindow = FormJS8Mail
        FormJS8Mail.setObjectName("FormJS8Mail")
        FormJS8Mail.resize(835, 215)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        FormJS8Mail.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormJS8Mail.setWindowIcon(icon)
        self.lineEdit = QtWidgets.QLineEdit(FormJS8Mail)
        self.lineEdit.setGeometry(QtCore.QRect(160, 50, 221, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.lineEdit.setMaxLength(40)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(FormJS8Mail)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 481, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(60)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(FormJS8Mail)
        self.label.setGeometry(QtCore.QRect(58, 50, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FormJS8Mail)
        self.label_2.setGeometry(QtCore.QRect(70, 100, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(FormJS8Mail)
        self.pushButton.setGeometry(QtCore.QRect(494, 150, 111, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.transmit)
        self.pushButton_2 = QtWidgets.QPushButton(FormJS8Mail)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 150, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.MainWindow.close)

        self.retranslateUi(FormJS8Mail)
        QtCore.QMetaObject.connectSlotsByName(FormJS8Mail)
        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        #self.transmit()
        self.test_responder(timestamp)




    def retranslateUi(self, FormJS8Mail):
        _translate = QtCore.QCoreApplication.translate
        FormJS8Mail.setWindowTitle(_translate("FormJS8Mail", "CommStat JS8Mail "))
        self.label.setText(_translate("FormJS8Mail", "Email Address : "))
        self.label_2.setText(_translate("FormJS8Mail", "Email Body :"))
        self.pushButton.setText(_translate("FormJS8Mail", "Transmit"))
        self.pushButton_2.setText(_translate("FormJS8Mail", "Cancel"))

    def prGreen(self,prt):
            print(f"\033[92m{prt}\033[00m")

    def prYellow(self,prt):
        print(f"\033[93m{prt}\033[00m")

    def prRed(self,prt):
        print(f"\033[91m{prt}\033[00m")

    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
        global timestamp
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
            state = format(systeminfo["state"])
            path = format(systeminfo["path"])
            serverip = format(systeminfo["server"])
            serverport = format(systeminfo["port"])
            selectedgroup = format(userinfo["selectedgroup"])
            print("\nIncoming CS Responder Request Timestamp:", sys.argv[1])
            timestamp = (sys.argv[1])

    def test_responder(self, timerec):
        global timestamp

        timestamp = str(timerec)
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        lastheard = timerec

        rowsQuery = "SELECT Count() FROM responder_Data Where timestamp  = '" + lastheard + "'"
        cur.execute(rowsQuery)
        numberOfRows = cur.fetchone()[0]
        if numberOfRows > 0:
            self.prYellow("Already responded to this CS Responder Request " + timestamp )
            cur.close()
            sys.exit()



        else:
            #print(timestamp)
            cur.execute(
                "INSERT OR REPLACE INTO responder_Data (timestamp) VALUES(? )",
                (timestamp,))
            conn.commit()
            print("Added CS Responder timestamp to database  \n \n")
            cur.close()
            self.transmit()




    def transmit(self):
            #emailcmd = "@APRSIS CMD :EMAIL-2  :";
            #emailtail = "{03}";
            message = ("@"+selectedgroup+", "+state+" "+grid+", CS1")
            messageType = js8callAPIsupport.TYPE_TX_SEND
            #mode = "EMAIL-2"
            #mode = mode.ljust(9)
            messageString = message  # mode+" "+self.tocall.get()+" "+text
            self.prGreen("CS1 Station Response Transmitted")
            self.sendMessage(messageType, messageString)
            self.closeapp()

            sys.exit()

    def closeapp(self):
        self.MainWindow.close()






    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormJS8Mail = QtWidgets.QWidget()
    ui = Ui_FormJS8Mail()
    ui.setupUi(FormJS8Mail)
    #FormJS8Mail.show()
    sys.exit(app.exec_())




