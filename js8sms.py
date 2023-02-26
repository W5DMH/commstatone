
import os
from configparser import ConfigParser
import re
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


import js8callAPIsupport

serverip = ""
serverport = ""


class Ui_FormJS8SMS(object):
    def setupUi(self, FormJS8SMS):
        self.MainWindow = FormJS8SMS
        FormJS8SMS.setObjectName("FormJS8SMS")
        FormJS8SMS.resize(835, 215)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        FormJS8SMS.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormJS8SMS.setWindowIcon(icon)
        self.lineEdit = QtWidgets.QLineEdit(FormJS8SMS)
        self.lineEdit.setGeometry(QtCore.QRect(160, 50, 113, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(FormJS8SMS)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 481, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setMaxLength(67)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(FormJS8SMS)
        self.label.setGeometry(QtCore.QRect(8, 50, 141, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FormJS8SMS)
        self.label_2.setGeometry(QtCore.QRect(48, 100, 101, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(FormJS8SMS)
        self.pushButton.setGeometry(QtCore.QRect(530, 150, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.transmit)

        self.pushButton_2 = QtWidgets.QPushButton(FormJS8SMS)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 150, 75, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.MainWindow.close)

        self.retranslateUi(FormJS8SMS)
        QtCore.QMetaObject.connectSlotsByName(FormJS8SMS)
        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))

        self.MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )



    def retranslateUi(self, FormJS8SMS):
        _translate = QtCore.QCoreApplication.translate
        FormJS8SMS.setWindowTitle(_translate("FormJS8SMS", "CommStat JS8SMS "))
        self.lineEdit.setInputMask(_translate("FormJS8SMS", "999-999-9999"))
        self.label.setText(_translate("FormJS8SMS", "Cellular Phone Number : "))
        self.label_2.setText(_translate("FormJS8SMS", "Text Message : "))
        self.pushButton.setText(_translate("FormJS8SMS", "Transmit"))
        self.pushButton_2.setText(_translate("FormJS8SMS", "Cancel"))
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

        phone = format(self.lineEdit.text())
        txtmsg = self.lineEdit_2.text()
        if len(phone) > 10:
            #if re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            print("This is a valid phone number")


        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("email address is not valid!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(txtmsg) < 8:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("email body is too short min 8 characters!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        else:

            smscmd = "@APRSIS CMD :SMSGTE   :@"
            smstail = "{04}";
            message = "" + smscmd + "" + phone + "  " + txtmsg + " " + smstail+""
            messageType = js8callAPIsupport.TYPE_TX_SETMESSAGE
            mode = "EMAIL-2"
            mode = mode.ljust(9)
            messageString = message  # mode+" "+self.tocall.get()+" "+text
            print("we got this far"+message)

            self.sendMessage(messageType, messageString)
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX TX")
            msg.setText("CommStatX will transmit : " + message)
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
    FormJS8SMS = QtWidgets.QWidget()
    ui = Ui_FormJS8SMS()
    ui.setupUi(FormJS8SMS)
    FormJS8SMS.show()
    sys.exit(app.exec_())
