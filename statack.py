import os
from configparser import ConfigParser
import re
from time import strftime
#from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime
import js8callAPIsupport
#import folium
import sqlite3
import io


serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""
acklist = ""
selectedfwd = ""

class Ui_FormStatack(object):
    def setupUi(self, FormStatack):
        self.MainWindow = FormStatack
        FormStatack.setObjectName("FormStatack")
        FormStatack.resize(950, 500)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormStatack.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormStatack.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(FormStatack)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(FormStatack)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.pushButton = QtWidgets.QPushButton(FormStatack)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(FormStatack)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 2)
        self.tableWidget = QtWidgets.QTableWidget(FormStatack)
        self.tableWidget.setObjectName("tableWidget")
        #self.tableWidget.setColumnCount(0)
        #self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(FormStatack)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(FormStatack)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 4, 2)

        self.pushButton_4 = QtWidgets.QPushButton(FormStatack)
        #self.pushButton_4.setGeometry(QtCore.QRect(350, 475, 131, 31))
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(FormStatack)
        #self.pushButton_4.setGeometry(QtCore.QRect(350, 475, 131, 31))
        self.gridLayout.addWidget(self.pushButton_5, 3, 2, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")


        self.tableWidget.clicked.connect(self.on_Click)

        self.getConfig()
        self.loadData()



        self.serveripad = serverip
        self.servport = int(serverport)
        self.api = js8callAPIsupport.js8CallUDPAPICalls((self.serveripad),
                                                        int(self.servport))
        self.pushButton_2.clicked.connect(self.closeapp)
        self.pushButton.clicked.connect(self.transmit)
        self.pushButton_4.clicked.connect(self.fwd_tx)
        self.pushButton_5.clicked.connect(self.delete_sr)



        self.retranslateUi(FormStatack)
        QtCore.QMetaObject.connectSlotsByName(FormStatack)

    def retranslateUi(self, FormStatack):
        _translate = QtCore.QCoreApplication.translate
        FormStatack.setWindowTitle(_translate("FormStatack", "CommStat StatRep Ack"))
        self.label_2.setText(_translate("FormStatack", "Selected Callsigns for ACK :"))
        self.pushButton.setText(_translate("FormStatack", "Transmit"))
        #self.label.setText(_translate("FormStatack", ""))
        self.pushButton_2.setText(_translate("FormStatack", "Cancel"))
        self.pushButton_4.setText(_translate("FormStatack", "Forward Selected StatRep"))
        self.pushButton_5.setText(_translate("FormStatack", "Delete Selected StatRep"))


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
            labeltext = ("Currently Active Group : " + selectedgroup)
            self.label.setText(labeltext)
            self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


    def loadData(self):
        #self.tableWidget = QtWidgets.QTableWidget(FormStatack)
        connection = sqlite3.connect('traffic.db3')
        query = """SELECT datetime, SRid, callsign, grid, prec, status, comments FROM StatRep_Data where groupname = ?"""
        result = connection.execute(query,(selectedgroup,))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(7)
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
            str("Date Time UTC ;ID ;Callsign; Grid ; Priority; Stat; Remarks").split(
                ";"))
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setVisible(False)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)
        # header.horizontalHeaderStretchLastSection = True
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.sortItems(0, QtCore.Qt.DescendingOrder)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 4)
        print("loadData completed")
        connection.close()

    def fwd_tx(self):
        global selectedfwd
        global acklist
        global selectedgroup
        #selectedfwd = int(selectedfwd)
        acklist_len = len(acklist)
        #print("here is length of selectedfwd "+str(acklist_len))
        #print("here is the record id "+str(selectedfwd))
        if acklist_len > 10:

            msg = QMessageBox()
            msg.setWindowTitle("CommStatX StatRep Saved")
            msg.setText("It appears you have made more than one StatRep selection, Commstat cannot forward more than one StatRep ID :" )
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()
            acklist = ""
            self.lineEdit.setText("")
            return



        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()

        #cur.execute(
        #    "INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        #    (date, call, group, grid, incidenceno, prec2, status, commpwr, pubwtr, med, ota, trav, net, fuel, food,
        #     crime, civil, political, comments))
        rowsQuery = "SELECT Count() FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
        cur.execute(rowsQuery)

        numberOfRows = cur.fetchone()[0]

        if numberOfRows == 1:
            dateq = "SELECT date FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(dateq)
            dateq = cur.fetchone()[0]
            gridq = "SELECT grid FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(gridq)
            gridq = cur.fetchone()[0]
            precq = "SELECT prec FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(precq)
            precq = cur.fetchone()[0]
            if (precq == "Routine"):
                precq = "1"
            elif (precq == "Priority"):
                precq = "2"
            elif (precq == "Immediate"):
                precq = "3"
            elif (precq == "Flash"):
                precq = "4"
            else:
                msg = QMessageBox()
                msg.setWindowTitle("CommStat error")
                msg.setText("Precedence is incorrect, cannot continue!")
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                x = msg.exec_()  # this will show our messagebox
                return
            incidencenoq = "SELECT SRid FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(incidencenoq)
            incidencenoq = cur.fetchone()[0]
            #print(incidencenoq)


            statusq = "SELECT status FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(statusq)
            statusq = cur.fetchone()[0]
            #print(statusq)



            commpwrq = "SELECT commpwr FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(commpwrq)
            commpwrq = cur.fetchone()[0]
            #print(commpwrq)

            pubwtrq = "SELECT pubwtr FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(pubwtrq)
            pubwtrq = cur.fetchone()[0]
            #print(pubwtrq)


            medq = "SELECT med FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(medq)
            medq = cur.fetchone()[0]


            otaq = "SELECT ota FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(otaq)
            otaq = cur.fetchone()[0]


            travq = "SELECT trav FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(travq)
            travq = cur.fetchone()[0]


            netq = "SELECT net FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(netq)
            netq = cur.fetchone()[0]


            fuelq = "SELECT fuel FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(fuelq)
            fuelq = cur.fetchone()[0]


            foodq = "SELECT food FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(foodq)
            foodq = cur.fetchone()[0]


            crimeq = "SELECT crime FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(crimeq)
            crimeq = cur.fetchone()[0]


            civilq = "SELECT civil FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(civilq)
            civilq = cur.fetchone()[0]


            politicalq = "SELECT political FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(politicalq)
            politicalq = cur.fetchone()[0]
            #print(politicalq)


            commentsq = "SELECT comments FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(commentsq)
            commentsq = cur.fetchone()[0]
            #print(commentsq)

            callq = "SELECT callsign FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
            cur.execute(callq)
            callq = cur.fetchone()[0]
            #print(callq)
            cur.close()






        selectedgroup1 = "@"+selectedgroup


        message = "@"+ selectedgroup + " ," + gridq + "," + precq + "," + incidencenoq + "," + statusq + commpwrq + pubwtrq + medq + otaq + travq + netq + fuelq + foodq + crimeq + civilq + politicalq + "," + commentsq + ","+callq+",{F%}" ""
        messageType = js8callAPIsupport.TYPE_TX_SEND
        messageString = message

        #print(message)

        self.sendMessage(messageType, messageString)

        self.closeapp()




    def on_Click(self):
        global acklist
        global selectedfwd
        index=(self.tableWidget.selectionModel().currentIndex())
        value = index.sibling(index.row(),2).data()
        selectedfwd = index.sibling(index.row(),1).data()
        acklist = acklist+ " * "+value
        self.lineEdit.setText("StatRep Received from : "+acklist)

    def transmit(self):
        global selectedgroup
        global callsign
        global acklist


        

        comments1 = "StatRep Received   "+ acklist
        comments = re.sub("[^A-Za-z0-9*\-\s]+", " ", comments1)

        if len(comments) < 5 :
            msg = QMessageBox()
            msg.setWindowTitle("CommStatX error")
            msg.setText( "Text too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox

            return
        group = "@"+selectedgroup
        message = "" + group + " " + comments + ""
        #message = ""+group + " ," + comments + ""
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
        acklist = ""
        self.closeapp()

    def delete_sr(self):
        global selectedfwd
        global acklist
        global selectedgroup
        #selectedfwd = int(selectedfwd)
        acklist_len = len(acklist)
        #print("here is length of selectedfwd "+str(acklist_len))
        #print("here is the record id "+str(selectedfwd))
        if acklist_len > 10:

            msg = QMessageBox()
            msg.setWindowTitle("CommStat StatRep Operation ")
            msg.setText("It appears you have made more than one StatRep selection, Commstat cannot Delete more than one StatRep ID :" )
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()
            acklist = ""
            self.lineEdit.setText("")
            return
        #print (acklist)
        #print (selectedfwd)
        #conn = sqlite3.connect("traffic.db3")
        #cur = conn.cursor()


        #cur.execute(
        #    "INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        #    (date, call, group, grid, incidenceno, prec2, status, commpwr, pubwtr, med, ota, trav, net, fuel, food,
        #     crime, civil, political, comments))
        #rowsQuery = "DELETE FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
        #cur.execute(rowsQuery)

        conn = sqlite3.connect("traffic.db3")
        cur = conn.cursor()

        # cur.execute(
        #    "INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        #    (date, call, group, grid, incidenceno, prec2, status, commpwr, pubwtr, med, ota, trav, net, fuel, food,
        #     crime, civil, political, comments))
        rowsQuery = "DELETE FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
        cur.execute(rowsQuery)
        conn.commit()
        cur.close()
        print("Deleted SR " + selectedfwd)
        selectedfwd = ""

        self.loadData()

        conn.close()

        #self.msgWarning = QMessageBox()
        # Set the Warning icon
        #self.msgWarning.setIcon(QMessageBox.Warning)
        # Set the main message
        #self.msgWarning.setText("You are about to permanently delete record :"+selectedfwd+" are you sure you want to continue ?")
        # Set two buttons for the message box
        #self.msgWarning.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # Call the custom method on button clicked
        #self.msgWarning.buttonClicked.connect(self.msgButton)
        # Set the title of the window
        #self.msgWarning.setWindowTitle("Warning Message")
        # Display the message box
        #self.msgWarning.show()

    # Define function for the buttons
    #def msgButton(self, i):
    #    global selectedfwd
    #    global acklist
    #    global selectedgroup
    #    if i.text() == 'OK':
    #        print("OK Button is pressed.")
     #       conn = sqlite3.connect("traffic.db3")
     #       cur = conn.cursor()

            # cur.execute(
            #    "INSERT INTO StatRep_Data(datetime,callsign,groupname, grid, SRid, prec,status, commpwr, pubwtr,med, ota, trav, net, fuel, food, crime, civil, political, comments) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            #    (date, call, group, grid, incidenceno, prec2, status, commpwr, pubwtr, med, ota, trav, net, fuel, food,
            #     crime, civil, political, comments))
      #      rowsQuery = "DELETE FROM StatRep_Data Where SRid  = '" + selectedfwd + "'"
      #      cur.execute(rowsQuery)
      #      conn.commit()
        #    cur.close()
        #
        #    selectedfwd = ""
        #    self.loadData()

       # else:
       #     print("Cancel Button is pressed.")
       #     selectedfwd = ""
        #    acklist = ""
        #    return

        #QMessageBox.question(self, '', "You are about to permanently delete record :"+selectedfwd+" are you sure you want to continue ?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #x = QMessageBox.exec_()
        #if msg == 'Yes':
            #conn.commit()
        #else :
        #    self.closeapp()

       # conn.close()




    def closeapp(self):
        #self.MainWindow.close()
        global acklist
        acklist = ""
        selectedfwd =""
        self.lineEdit.setText("")
        

    def sendMessage(self, messageType, messageText):
        self.api.sendMessage(messageType, messageText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormStatack = QtWidgets.QWidget()
    ui = Ui_FormStatack()
    ui.setupUi(FormStatack)
    FormStatack.show()
    sys.exit(app.exec_())
