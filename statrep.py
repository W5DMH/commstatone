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
stat_id =  ""

class Ui_FormStatRep(object):
    def setupUi(self, FormStatRep):
        self.MainWindow = FormStatRep
        FormStatRep.setObjectName("FormStatRep")
        FormStatRep.resize(808, 768)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FormStatRep.sizePolicy().hasHeightForWidth())
        FormStatRep.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormStatRep.setWindowIcon(icon)

        self.pushButton = QtWidgets.QPushButton(FormStatRep)
        self.pushButton.setGeometry(QtCore.QRect(500, 475, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_3 = QtWidgets.QPushButton(FormStatRep)
        self.pushButton_3.setGeometry(QtCore.QRect(250, 475, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(FormStatRep)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 475, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")



        self.pushButton_2 = QtWidgets.QPushButton(FormStatRep)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 474, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")



        self.label = QtWidgets.QLabel(FormStatRep)
        self.label.setGeometry(QtCore.QRect(20, 0, 781, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("statrep-4v-top.png"))
        self.label.setObjectName("label")
        
       
        
        
        

        self.lineEditToGrp = QtWidgets.QLineEdit(FormStatRep)
        self.lineEditToGrp.setGeometry(QtCore.QRect(29, 142, 214, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditToGrp.setFont(font)
        self.lineEditToGrp.setObjectName("lineEditToGrp")
        self.lineEditToGrp.setEnabled(False)
        self.lineEditFrom = QtWidgets.QLineEdit(FormStatRep)
        self.lineEditFrom.setGeometry(QtCore.QRect(281, 141, 213, 22))
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditFrom.setFont(font)
        self.lineEditFrom.setObjectName("lineEditFrom")
        #self.lineEditFrom.setEnabled(False)
        self.lineEditID = QtWidgets.QLineEdit(FormStatRep)
        self.lineEditID.setGeometry(QtCore.QRect(28, 193, 354, 22))
        
        self.comboBoxPrecedent = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxPrecedent.setGeometry(QtCore.QRect(534, 142, 152, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxPrecedent.setFont(font)
        self.comboBoxPrecedent.setObjectName("comboBoxPrecedent")
        self.comboBoxPrecedent.addItem('')
        self.comboBoxPrecedent.addItem('Routine')
        self.comboBoxPrecedent.addItem('Priority')
        self.comboBoxPrecedent.addItem('Immediate')
        self.comboBoxPrecedent.addItem('Flash')
        
        

        self.lineEditGrid = QtWidgets.QLineEdit(FormStatRep)
        self.lineEditGrid.setGeometry(QtCore.QRect(449, 193, 281, 22))
        
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditGrid.setFont(font)
        self.lineEditGrid.setObjectName("lineEditGrid")
        #self.lineEditGrid.setEnabled(False)
        

        
        self.comboBoxStatus = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxStatus.setGeometry(QtCore.QRect(30, 244, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxStatus.setFont(font)
        self.comboBoxStatus.setObjectName("comboBoxStatus")
        self.comboBoxStatus.addItem('')
        self.comboBoxStatus.addItem('Green')
        self.comboBoxStatus.addItem('Yellow')
        self.comboBoxStatus.addItem('Red')
        
        self.comboBoxPower = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxPower.setGeometry(QtCore.QRect(305, 244, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxPower.setFont(font)
        self.comboBoxPower.setObjectName("comboBoxPower")
        self.comboBoxPower.addItem('')
        self.comboBoxPower.addItem('Green')
        self.comboBoxPower.addItem('Yellow')
        self.comboBoxPower.addItem('Red')
        
        self.comboBoxWater = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxWater.setGeometry(QtCore.QRect(547, 244, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxWater.setFont(font)
        self.comboBoxWater.setObjectName("comboBoxWater")
        self.comboBoxWater.addItem('')
        self.comboBoxWater.addItem('Green')
        self.comboBoxWater.addItem('Yellow')
        self.comboBoxWater.addItem('Red')
        
        self.comboBoxMedical = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxMedical.setGeometry(QtCore.QRect(30, 291, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxMedical.setFont(font)
        self.comboBoxMedical.setObjectName("comboBoxMedical")
        self.comboBoxMedical.addItem('')
        self.comboBoxMedical.addItem('Green')
        self.comboBoxMedical.addItem('Yellow')
        self.comboBoxMedical.addItem('Red')
        self.comboBoxComms = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxComms.setGeometry(QtCore.QRect(305, 291, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxComms.setFont(font)
        self.comboBoxComms.setObjectName("comboBoxComms")
        self.comboBoxComms.addItem('')
        self.comboBoxComms.addItem('Green')
        self.comboBoxComms.addItem('Yellow')
        self.comboBoxComms.addItem('Red')
        self.comboBoxTravel = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxTravel.setGeometry(QtCore.QRect(547, 291, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxTravel.setFont(font)
        self.comboBoxTravel.setObjectName("comboBoxTravel")
        self.comboBoxTravel.addItem('')
        self.comboBoxTravel.addItem('Green')
        self.comboBoxTravel.addItem('Yellow')
        self.comboBoxTravel.addItem('Red')
        
        self.comboBoxInternet = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxInternet.setGeometry(QtCore.QRect(30, 338, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxInternet.setFont(font)
        self.comboBoxInternet.setObjectName("comboBoxInternet")
        self.comboBoxInternet.addItem('')
        self.comboBoxInternet.addItem('Green')
        self.comboBoxInternet.addItem('Yellow')
        self.comboBoxInternet.addItem('Red')
        self.comboBoxFuel = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxFuel.setGeometry(QtCore.QRect(305, 338, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxFuel.setFont(font)
        self.comboBoxFuel.setObjectName("comboBoxFuel")
        self.comboBoxFuel.addItem('')
        self.comboBoxFuel.addItem('Green')
        self.comboBoxFuel.addItem('Yellow')
        self.comboBoxFuel.addItem('Red')
        self.comboBoxFood = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxFood.setGeometry(QtCore.QRect(547, 338, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxFood.setFont(font)
        self.comboBoxFood.setObjectName("comboBoxFood")
        self.comboBoxFood.addItem('')
        self.comboBoxFood.addItem('Green')
        self.comboBoxFood.addItem('Yellow')
        self.comboBoxFood.addItem('Red')
        
        self.comboBoxCrime = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxCrime.setGeometry(QtCore.QRect(29, 385, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxCrime.setFont(font)
        self.comboBoxCrime.setObjectName("comboBoxCrime")
        self.comboBoxCrime.addItem('')
        self.comboBoxCrime.addItem('Green')
        self.comboBoxCrime.addItem('Yellow')
        self.comboBoxCrime.addItem('Red')
        self.comboBoxCivil = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxCivil.setGeometry(QtCore.QRect(305, 385, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxCivil.setFont(font)
        self.comboBoxCivil.setObjectName("comboBoxCivil")
        self.comboBoxCivil.addItem('')
        self.comboBoxCivil.addItem('Green')
        self.comboBoxCivil.addItem('Yellow')
        self.comboBoxCivil.addItem('Red')
        self.comboBoxPolitical = QtWidgets.QComboBox(FormStatRep)
        self.comboBoxPolitical.setGeometry(QtCore.QRect(547, 385, 130, 22))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.comboBoxPolitical.setFont(font)
        self.comboBoxPolitical.setObjectName("comboBoxPolitical")
        self.comboBoxPolitical.addItem('')
        self.comboBoxPolitical.addItem('Green')
        self.comboBoxPolitical.addItem('Yellow')
        self.comboBoxPolitical.addItem('Red')
        
        
        
        #put above this line 
        self.lineEdit = QtWidgets.QLineEdit(FormStatRep)
        self.lineEdit.setGeometry(QtCore.QRect(30, 434, 706, 24))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        
        
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEditID.setFont(font)
        self.lineEditID.setObjectName("lineEditID")
        self.lineEditID.setEnabled(False)
        
        self.textBrowser = QtWidgets.QTextBrowser(FormStatRep)
        self.textBrowser.setGeometry(QtCore.QRect(17, 530, 776, 230))
        self.textBrowser.setSource(QtCore.QUrl("CommStatStatrep_V1.6.html"))
        self.textBrowser.setObjectName("textBrowser")
        
        
        
        self.label.raise_()
        self.comboBoxTravel.raise_()
        self.comboBoxCivil.raise_()
        self.comboBoxFood.raise_()
        self.lineEditFrom.raise_()
        self.comboBoxMedical.raise_()
        self.comboBoxStatus.raise_()
        self.comboBoxFuel.raise_()
        self.lineEdit.raise_()
        self.comboBoxPower.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.lineEditID.raise_()
        self.comboBoxComms.raise_()
        self.comboBoxCrime.raise_()
        self.lineEditGrid.raise_()
        self.comboBoxPrecedent.raise_()
        self.comboBoxWater.raise_()
        self.lineEditToGrp.raise_()
        self.comboBoxInternet.raise_()
        self.pushButton.raise_()
        self.comboBoxPolitical.raise_()
        self.textBrowser.raise_()

        self.retranslateUi(FormStatRep)
        QtCore.QMetaObject.connectSlotsByName(FormStatRep)
        
        self.find_statrep_id()

        self.getConfig()
        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.MainWindow.close)
        self.pushButton.clicked.connect(self.transmit)
        self.pushButton_3.clicked.connect(self.save_only)
        self.pushButton_4.clicked.connect(self.all_green)

        self.MainWindow.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )



    def retranslateUi(self, FormStatRep):
        _translate = QtCore.QCoreApplication.translate
        FormStatRep.setWindowTitle(_translate("FormStatRep", "Commstat StatRep"))
        self.pushButton.setText(_translate("FormStatRep", "Transmit"))
        self.pushButton_2.setText(_translate("FormStatRep", "Cancel"))
        self.pushButton_3.setText(_translate("FormStatRep", "Save Only"))
        self.pushButton_4.setText(_translate("FormStatRep", "All Green"))

    def getConfig(self):
        global serverip
        global serverport
        global grid
        global callsign
        global selectedgroup
        global stat_id
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
            self.lineEditFrom.setText(callsign)
            self.lineEditToGrp.setText(selectedgroup)
            self.lineEditGrid.setText(grid)
            randnum = random.randint(100, 999)
            #self.lineEditID.setText(str(randnum))
            self.lineEditID.setText(stat_id)

    def save_only(self):
        group = format(self.lineEditToGrp.text())
        group = group.upper()
        call = format(self.lineEditFrom.text())
        call = call.upper()
        grid = format(self.lineEditGrid.text())
        grid = grid.upper()
        prec = format(self.comboBoxPrecedent.currentText())
        prec2 = format(self.comboBoxPrecedent.currentText())
        incidenceno = format(self.lineEditID.text())
        status = format(self.comboBoxStatus.currentText())
        commpwr = format(self.comboBoxPower.currentText())
        pubwtr = format(self.comboBoxWater.currentText())
        med = format(self.comboBoxMedical.currentText())
        ota = format(self.comboBoxComms.currentText())
        trav = format(self.comboBoxTravel.currentText())
        net = format(self.comboBoxInternet.currentText())
        fuel = format(self.comboBoxFuel.currentText())
        food = format(self.comboBoxFood.currentText())
        crime = format(self.comboBoxCrime.currentText())
        civil = format(self.comboBoxCivil.currentText())
        political = format(self.comboBoxPolitical.currentText())
        comments1 = format(self.lineEdit.text())
        comments1 = comments1.upper()

        #comments = re.Replace(comments1, @ "[^A-Za-z0-9*\-\s]+", "");
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(group) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Group Name too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
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
            msg.setText("Does not meet callsign structure!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if len(comments) > 60 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Remarks too long, please abbreviate")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(comments) < 1:
            comments = "NTR"
        if len(grid) < 4:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Grid is not valid")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if "Green" in status:
            status = "1"
        elif ("Yellow" in status):
            status = "2"
        elif ("Red" in status):
            status = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (commpwr == "Green"):
            commpwr = "1"
        elif (commpwr == "Yellow"):
            commpwr = "2"
        elif (commpwr == "Red"):
            commpwr = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (pubwtr == "Green"):
            pubwtr = "1"
        elif (pubwtr == "Yellow"):
            pubwtr = "2"
        elif (pubwtr == "Red"):
            pubwtr = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (med == "Green"):
            med = "1"
        elif (med == "Yellow"):
            med = "2"
        elif (med == "Red"):
            med = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (ota == "Green"):
            ota = "1"
        elif (ota == "Yellow"):
            ota = "2"
        elif (ota == "Red"):
            ota = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (trav == "Green"):
            trav = "1"
        elif (trav == "Yellow"):
            trav = "2"
        elif (trav == "Red"):
            trav = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (net == "Green"):
            net = "1"
        elif (net == "Yellow"):
            net = "2"
        elif (net == "Red"):
            net = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (fuel == "Green"):
            fuel = "1"
        elif (fuel == "Yellow"):
            fuel = "2"
        elif (fuel == "Red"):
            fuel = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (food == "Green"):
            food = "1"
        elif (food == "Yellow"):
            food = "2"
        elif (food == "Red"):
            food = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (crime == "Green"):
            crime = "1"
        elif (crime == "Yellow"):
            crime = "2"
        elif (crime == "Red"):
            crime = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (civil == "Green"):
            civil = "1"
        elif (civil == "Yellow"):
            civil = "2"
        elif (civil == "Red"):
            civil = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (political == "Green"):
            political = "1"
        elif (political == "Yellow"):
            political = "2"
        elif (political == "Red"):
            political = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (prec == "Routine"):
            prec = "1"
        elif (prec == "Priority"):
            prec = "2"
        elif (prec == "Immediate"):
            prec = "3"
        elif (prec == "Flash"):
            prec = "4"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return



        selectedgroup1 = "@"+selectedgroup


        message = "" + selectedgroup1 + " ," + grid + "," + prec + "," + incidenceno + "," + status + commpwr + pubwtr + med + ota + trav + net + fuel + food + crime + civil + political + "," + comments + ",{&%}" ""
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        #self.sendMessage(messageType, messageString)
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX StatRep Saved")
        msg.setText("CommStatX has saved : " + message)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()

        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        conn.set_trace_callback(print)
        cur.execute("INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date,call,group,grid,incidenceno,prec2,status,commpwr,pubwtr,med,ota,trav,net ,fuel,food,crime,civil,political,comments))
        conn.commit()
        cur.close()

        datafile = open("copyDIRECTED.TXT", "w")
        datafile.write("blank line \n" )
        datafile.close()

        self.closeapp()

    def all_green(self):
        group = format(self.lineEditToGrp.text())
        group = group.upper()
        call = format(self.lineEditFrom.text())
        call = call.upper()
        grid = format(self.lineEditGrid.text())
        grid = grid.upper()
        prec = format(self.comboBoxPrecedent.setCurrentText("Routine"))
        prec = "1"# format(self.comboBoxPrecedent.currentText("Routine"))
        prec2 = format(self.comboBoxPrecedent.currentText())
        incidenceno = format(self.lineEditID.text())
        status = "1" # format(self.comboBoxStatus.setCurrentText("Green"))
        commpwr = "1" # format(self.comboBoxPower.setCurrentText("Green"))
        pubwtr = "1" # format(self.comboBoxWater.setCurrentText("Green"))
        med = "1" # format(self.comboBoxMedical.setCurrentText("Green"))
        ota = "1" # format(self.comboBoxComms.setCurrentText("Green"))
        trav = "1" # format(self.comboBoxTravel.setCurrentText("Green"))
        net = "1" # format(self.comboBoxInternet.setCurrentText("Green"))
        fuel = "1" # format(self.comboBoxFuel.setCurrentText("Green"))
        food = "1" # format(self.comboBoxFood.setCurrentText("Green"))
        crime = "1" # format(self.comboBoxCrime.setCurrentText("Green"))
        civil = "1" # format(self.comboBoxCivil.setCurrentText("Green"))
        political = "1" # format(self.comboBoxPolitical.setCurrentText("Green"))
        format(self.lineEdit.setText("NTR"))
        comments1 = format(self.lineEdit.text())
        comments1 = comments1.upper()
        comments = comments1

        format(self.comboBoxStatus.setCurrentText("Green"))
        format(self.comboBoxPower.setCurrentText("Green"))
        format(self.comboBoxWater.setCurrentText("Green"))
        format(self.comboBoxMedical.setCurrentText("Green"))
        format(self.comboBoxComms.setCurrentText("Green"))
        format(self.comboBoxTravel.setCurrentText("Green"))
        format(self.comboBoxInternet.setCurrentText("Green"))
        format(self.comboBoxFuel.setCurrentText("Green"))
        format(self.comboBoxFood.setCurrentText("Green"))
        format(self.comboBoxCrime.setCurrentText("Green"))
        format(self.comboBoxCivil.setCurrentText("Green"))
        format(self.comboBoxPolitical.setCurrentText("Green"))
        #format(self.lineEdit.setText("NTR"))








        ##comments = re.Replace(comments1, @ "[^A-Za-z0-9*\-\s]+", "");
        #comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(group) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Group Name too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(call) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Callsign too short")
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

        if len(comments) > 60 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Remarks too long, please abbreviate")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(comments) < 1:
            comments = "NTR"
        if len(grid) < 4:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Grid is not valid")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return




        selectedgroup1 = "@"+selectedgroup


        message = "" + selectedgroup1 + " ," + grid + "," + prec + "," + incidenceno + "," + status + commpwr + pubwtr + med + ota + trav + net + fuel + food + crime + civil + political + "," + comments + ",{&%}" ""
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message
        #print(message)


        #now = QDateTime.currentDateTime()
        #date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        #conn = sqlite3.connect("traffic.db3")
        #cur = conn.cursor()
        #conn.set_trace_callback(print)
        #cur.execute("INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date,call,group,grid,incidenceno,prec2,status,commpwr,pubwtr,med,ota,trav,net ,fuel,food,crime,civil,political,comments))
        #conn.commit()
        #cur.close()

        datafile = open("copyDIRECTED.TXT", "w")
        datafile.write("blank line \n" )
        datafile.close()

        #self.closeapp()



    def transmit(self):
        global selectedgroup
        group = format(self.lineEditToGrp.text())
        group = group.upper()
        call = format(self.lineEditFrom.text())
        call = call.upper()
        grid = format(self.lineEditGrid.text())
        grid = grid.upper()
        prec = format(self.comboBoxPrecedent.currentText())
        prec2 = format(self.comboBoxPrecedent.currentText())
        incidenceno = format(self.lineEditID.text())
        status = format(self.comboBoxStatus.currentText())
        commpwr = format(self.comboBoxPower.currentText())
        pubwtr = format(self.comboBoxWater.currentText())
        med = format(self.comboBoxMedical.currentText())
        ota = format(self.comboBoxComms.currentText())
        trav = format(self.comboBoxTravel.currentText())
        net = format(self.comboBoxInternet.currentText())
        fuel = format(self.comboBoxFuel.currentText())
        food = format(self.comboBoxFood.currentText())
        crime = format(self.comboBoxCrime.currentText())
        civil = format(self.comboBoxCivil.currentText())
        political = format(self.comboBoxPolitical.currentText())
        comments1 = format(self.lineEdit.text())
        comments1 = comments1.upper()

        #comments = re.Replace(comments1, @ "[^A-Za-z0-9*\-\s]+", "");
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(group) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Group Name too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(callsign) < 4 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Callsign too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(comments) > 60 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Remarks too long, please abbreviate")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if len(comments) < 1:
            comments = "NTR"
        if len(grid) < 4:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("Grid is not valid")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return

        if "Green" in status:
            status = "1"
        elif ("Yellow" in status):
            status = "2"
        elif ("Red" in status):
            status = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (commpwr == "Green"):
            commpwr = "1"
        elif (commpwr == "Yellow"):
            commpwr = "2"
        elif (commpwr == "Red"):
            commpwr = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (pubwtr == "Green"):
            pubwtr = "1"
        elif (pubwtr == "Yellow"):
            pubwtr = "2"
        elif (pubwtr == "Red"):
            pubwtr = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (med == "Green"):
            med = "1"
        elif (med == "Yellow"):
            med = "2"
        elif (med == "Red"):
            med = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (ota == "Green"):
            ota = "1"
        elif (ota == "Yellow"):
            ota = "2"
        elif (ota == "Red"):
            ota = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (trav == "Green"):
            trav = "1"
        elif (trav == "Yellow"):
            trav = "2"
        elif (trav == "Red"):
            trav = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (net == "Green"):
            net = "1"
        elif (net == "Yellow"):
            net = "2"
        elif (net == "Red"):
            net = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (fuel == "Green"):
            fuel = "1"
        elif (fuel == "Yellow"):
            fuel = "2"
        elif (fuel == "Red"):
            fuel = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (food == "Green"):
            food = "1"
        elif (food == "Yellow"):
            food = "2"
        elif (food == "Red"):
            food = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (crime == "Green"):
            crime = "1"
        elif (crime == "Yellow"):
            crime = "2"
        elif (crime == "Red"):
            crime = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (civil == "Green"):
            civil = "1"
        elif (civil == "Yellow"):
            civil = "2"
        elif (civil == "Red"):
            civil = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (political == "Green"):
            political = "1"
        elif (political == "Yellow"):
            political = "2"
        elif (political == "Red"):
            political = "3"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        if (prec == "Routine"):
            prec = "1"
        elif (prec == "Priority"):
            prec = "2"
        elif (prec == "Immediate"):
            prec = "3"
        elif (prec == "Flash"):
            prec = "4"
        else:
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText("All boxes must have a selection!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return



        selectedgroup = "@"+selectedgroup


        message = "" + selectedgroup + " ," + grid + "," + prec + "," + incidenceno + "," + status + commpwr + pubwtr + med + ota + trav + net + fuel + food + crime + civil + political + "," + comments + ",{&%}" ""
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        self.sendMessage(messageType, messageString)
        #msg = QMessageBox()
        #msg.setWindowTitle("CommStatX TX")
        #msg.setText("CommStatX will transmit : " + message)
        #msg.setIcon(QMessageBox.Information)
        #msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        #x = msg.exec_()

        now = QDateTime.currentDateTime()
        date = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))
        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()
        conn.set_trace_callback(print)
        cur.execute("INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(date,call,group,grid,incidenceno,prec2,status,commpwr,pubwtr,med,ota,trav,net ,fuel,food,crime,civil,political,comments))
        conn.commit()
        cur.close()

        datafile = open("copyDIRECTED.TXT", "w")
        datafile.write("blank line \n" )
        datafile.close()

        self.closeapp()
        
    def find_statrep_id(self):
        global stat_id
        randnum = random.randint(100, 999)
        stat_id = (str(randnum))
        #stat_id = "902"

        try:
            sqliteConnection = sqlite3.connect('traffic.db3')
            cursor = sqliteConnection.cursor()
           # print("Connected to SQLite")
            sqlite_select_query = 'SELECT SRid FROM StatRep_Data;'
            cursor.execute(sqlite_select_query)
            items = cursor.fetchall()

            for item in items:
                srid = item[0]
                #print(item)
                if stat_id in item:
                    print("StatRep random number failed, recycling and trying again")
                    cursor.close()
                    self.find_statrep_id()



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
    FormStatRep = QtWidgets.QWidget()
    ui = Ui_FormStatRep()
    ui.setupUi(FormStatRep)
    FormStatRep.show()
    sys.exit(app.exec_())
