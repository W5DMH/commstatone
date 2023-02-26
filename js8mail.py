
import re

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import js8callAPIsupport
from configparser import ConfigParser
import os


serverip = ""
serverport = ""

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





    def retranslateUi(self, FormJS8Mail):
        _translate = QtCore.QCoreApplication.translate
        FormJS8Mail.setWindowTitle(_translate("FormJS8Mail", "CommStat JS8Mail "))
        self.label.setText(_translate("FormJS8Mail", "Email Address : "))
        self.label_2.setText(_translate("FormJS8Mail", "Email Body :"))
        self.pushButton.setText(_translate("FormJS8Mail", "Transmit"))
        self.pushButton_2.setText(_translate("FormJS8Mail", "Cancel"))


    def getConfig(self):
        global serverip
        global serverport
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


    def transmit(self):

        email = format(self.lineEdit.text())
        body = self.lineEdit_2.text()
        if len(email) > 7:
            if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
                print("This is a valid email address")

            else:
                msg = QMessageBox()
                msg.setWindowTitle("CommStatX error")
                msg.setText("email address is not valid!")
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                x = msg.exec_()  # this will show our messagebox
                return
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("email address is not valid!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(body) < 8:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("email body is too short min 8 characters!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        else:
            emailcmd = "@APRSIS CMD :EMAIL-2  :";
            emailtail = "{03}";
            message = ""+emailcmd+""+email+" "+body+""+emailtail+""
            messageType = js8callAPIsupport.TYPE_TX_SETMESSAGE
            mode = "EMAIL-2"
            mode = mode.ljust(9)
            messageString = message  # mode+" "+self.tocall.get()+" "+text

            self.sendMessage(messageType, messageString)
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX TX")
            msg.setText("CommStatX will transmit : "+message)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            self.closeapp()
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
    FormJS8Mail.show()
    sys.exit(app.exec_())




