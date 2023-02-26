import os
import webbrowser

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QDateTimeEdit, QLineEdit, QPushButton, QTableWidget, \
    QWidget, QFileDialog, QMessageBox, QGridLayout, QCheckBox, QListView, QListWidget, QListWidgetItem, QVBoxLayout, QDialog

from PyQt5 import uic, QtCore, QtWidgets, QtGui, QtPrintSupport
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDateTime, Qt, QDate, Qt
import configparser
import sys
import sqlite3
import pandas as pd
import datetime
import folium
from datetime import datetime
import pandas as pd
import io
import re
import maidenhead as mh


start = ""
end = ""
loadflag = 0
statelist = ['CN', 'CM', 'DN', 'DM', 'DL', 'EN', 'EM', 'EL', 'FN', 'FM']

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.setStyleSheet('font-size: 12px')

        #load the ui file
        uic.loadUi("commdata2.ui", self)







        self.report_name = self.findChild(QLineEdit,"lineEditName")
        self.start_datetime = self.findChild(QDateTimeEdit,"dateTimeEditStart")
        self.end_datetime = self.findChild(QDateTimeEdit,"dateTimeEditEnd")
        self.exportdata = self.findChild(QPushButton,"pushButtonEX")
        self.importdata = self.findChild(QPushButton,"pushButtonIM")
        self.printdata = self.findChild(QPushButton,"pushButtonPrint")
        self.displaydata = self.findChild(QPushButton, "pushButtonLoad")
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.mapwidget = self.findChild(QWidget,"widget" )
        self.layout = self.findChild(QGridLayout,"gridLayout")
        self.state = self.findChild(QPushButton,"pushButtonstate")
        self.stateclose = self.findChild(QPushButton,'pushButtonclosestate')
        self.stateclear = self.findChild(QPushButton, 'pushButtonclearstate')
        self.stateslabel = self.findChild(QLabel,'labelstates')

        #self.listView = self.findChild(QListView, "listViewstate")
        #self.listView = QtGui.QListView(Dialog)
        #self.listView.setObjectName(_fromUtf8("listView"))



        #model = QtGui.QStandardItemModel()
        #self.listView.setModel(model)

        #for i in entries:
        #    item = QtGui.QStandardItem(i)
        #    model.appendRow(item)

        #self.gridLayout.addWidget(self.listView, 2, 2, 1, 1)

        self.green = self.findChild(QCheckBox, "checkBoxgreen")
        self.yellow = self.findChild(QCheckBox, "checkBoxyellow")
        self.red = self.findChild(QCheckBox, "checkBoxred")
        self.green.setChecked(True)
        self.yellow.setChecked(True)
        self.red.setChecked(True)


        #button / date activities
        self.importdata.clicked.connect(self.importcommstat)
        self.exportdata.clicked.connect(self.export_csv)
        #self.printdata.clicked.connect(self.printdisplay)
        self.displaydata.clicked.connect(self.loadData)
        #self.printdata = QtWidgets.QPushButton('Print', self)
        self.printdata.clicked.connect(self.buildreport)
        #self.buttonPreview = QtWidgets.QPushButton('Preview', self)
        #self.buttonPreview.clicked.connect(self.handlePreview)
        self.state.clicked.connect(self.stateselector)
        self.stateclose.hide()
        self.stateclear.hide()
        self.stateclose.clicked.connect(self.stateselected)
        self.stateclear.clicked.connect(self.stateclearsel)
        self.stateslabel.setText("All Grids Shown")




        now = QDateTime.currentDateTime()
        now = now.toUTC()

        self.start_datetime.setDateTime(now)
        self.end_datetime.setDateTime(now)


        # Show the application
        self.show()
        self.testload()

    def testload(self):
        now = QDateTime.currentDateTime()
        now = now.toUTC()
        beforetime = QDateTime.currentDateTime()
        before = beforetime.addDays(-30)
        before = before.toUTC()
        global start
        global end
        if loadflag > 0:
            print("SR Report Loaded")
        else:
            start = before.toString("yyyy-MM-dd HH:mm")
            #start = now.toString("yyyy-MM-dd HH:mm")
            end = now.toString("yyyy-MM-dd HH:mm")

            #self.start_datetime..toString("yyyy-MM-dd HH:mm"))
            #self.end_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))

            self.loadData()




    def importcommstat(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','', "Image files (*.jpg *.csv)")
        filetoopen = (fname[0])
        # load the data into a Pandas DataFrame
        importdata = pd.read_csv(filetoopen)
        # write the data to a sqlite table
        conn = sqlite3.connect('traffic.db3')
        importdata.to_sql('StatRep_Data_temp', conn, if_exists='replace', index=False)

        crossquery = ("INSERT OR REPLACE INTO StatRep_Data SELECT * FROM StatRep_Data_temp WHERE SRid != StatRep_Data_temp.SRid")
        #query = conn.execute("SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data WHERE groupname = ? AND datetime BETWEEN ? AND ?")
        #result = connection.execute(query, (selectedgroup, start, end))
        #print(crossquery)

        cur = conn.cursor()
        #cur.execute("INSERT OR REPLACE INTO StatRep_Data SELECT NULL, datetime, date, T1, freq, SRid, callsign, groupname, grid, prec, status, commpwr, pubwtr, med, ota,"
        #            " trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data_temp ")

        test = cur.execute("INSERT OR REPLACE INTO StatRep_Data SELECT NULL, datetime, date, T1, freq, callsign, groupname, grid, SRid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data_temp")
        conn.commit()
        #cur.execute("INSERT OR REPLACE INTO StatRep_Data SELECT * FROM StatRep_Data_temp")
        #print(test)



    def export_csv(self):
        global start
        global end
        global selectedgroup

        try:
            format_data = "%Y-%m-%d %H:%M"
            netstart = datetime.strptime(start, format_data)

            format_data = "%Y-%m-%d %H:%M"
            netend = datetime.strptime(end, format_data)

            netstartB = str(start.replace(" ", "-"))
            netstartB = netstartB.replace(":","-")
            net_data_name = ("Commstat_SR_Data_"+(netstartB)+".csv")
            print("Saved data file : "+net_data_name)

            conn = sqlite3.connect('traffic.db3')
            #clients = pd.read_sql_query( "SELECT datetime, SRid, callsign, groupname, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data WHERE groupname = ? AND datetime BETWEEN ? AND ?", conn, params=(selectedgroup, start, end))
            clients = pd.read_sql_query("SELECT * FROM StatRep_Data WHERE groupname = ? AND datetime BETWEEN ? AND ?",
                conn, params=(selectedgroup, start, end))
            path = os.path.join('reports', net_data_name)
            clients.to_csv(path, index=False)
            conn.close()
            print("Saved data file : " + net_data_name)
            msg = QMessageBox()
            msg.setWindowTitle("CommStat Data Export Success!")
            msg.setText("Commstat Data Export succeeded in saving : "+net_data_name)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox

        except Exception as ex:
            print("Failed to write file : "+str(ex))
            msg = QMessageBox()
            msg.setWindowTitle("CommStat Data Export Error")
            msg.setText("Commstat Data Export failed for : "+str(ex))
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return


    def readconfig(self):
        # Read config.ini file
        config_object = configparser.ConfigParser()
        config_object.read("config.ini")
        global callsign
        global callsignSuffix
        global group1
        global group2
        global grid
        global path
        global selectedgroup
        global OS_Directed

        # Get the password
        userinfo = config_object["USERINFO"]
        #print("callsign is {}".format(userinfo["callsign"]))
        #print("callsignsuffix is {}".format(userinfo["callsignsuffix"]))
        #print("group1 is {}".format(userinfo["group1"]))
        #print("group2 is {}".format(userinfo["group2"]))
        #print("grid is {}".format(userinfo["grid"]))
        systeminfo = config_object["DIRECTEDCONFIG"]
        #print("file path  is {}".format(systeminfo["path"]))
        callsign = format(userinfo["callsign"])
        callsignSuffix = format(userinfo["callsignsuffix"])
        group1 = format(userinfo["group1"])
        group2 = format(userinfo["group2"])
        grid = format(userinfo["grid"])
        #path1 = format(systeminfo["path"])
        #path = (path1+""+OS_Directed)
        selectedgroup = format(userinfo["selectedgroup"])
        #print("this is the new path :"+path)
        #print(selectedgroup)
        if (callsign =="NOCALL"):
            #self.settings_window()
            print("no callsign")

    def stateselector(self):
        global statelist
        statelist = []
        self.window = QWidget()
        self.listWidget = QListWidget()
        #listWidget.setSelectionMode(2)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.window.setFixedWidth(80)
        self.window.setWindowTitle("Select Grid(s)")

        #QListWidgetItem("Geeks", listWidget)
        #QListWidgetItem("For", listWidget)
        #QListWidgetItem("Geeks", listWidget)
        states = ['CN', 'CM', 'DN', 'DM', 'DL', 'EN', 'EM', 'EL', 'FN', 'FM']
        for state in states:
            QListWidgetItem(state ,self.listWidget)

        #listWidget.itemClicked.connect(self.Clicked)

        self.listWidget.itemClicked.connect(self.Clicked)

        self.window_layout = QVBoxLayout(self.window)
        self.window_layout.addWidget(self.listWidget)
        #self.window.setLayout(self.window_layout)
        self.gridLayout.addWidget(self.window, 2, 0, 1, 1)

        self.state.hide()
        self.stateclose.show()
        self.stateslabel.hide()


        #self.listView = QtGui.QListView(Dialog)
        #self.listView.setObjectName(_fromUtf8("listView"))

    def stateselected(self):
        self.listWidget.close()
        self.stateclose.hide()
        self.state.show()
        self.stateslabel.setText(str(statelist))
        self.stateslabel.show()
        self.stateclear.show()


    def Clicked(self):
        global statelist

        #QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())
        items = self.listWidget.selectedItems()
        #x = []
        for i in range(len(items)):
            statelist.append(str(self.listWidget.selectedItems()[i].text()))
            print(statelist)
        print (statelist)

    def stateclearsel(self):
        global statelist
        statelist = []
        msg = QMessageBox()
        msg.setWindowTitle("CommStat Report Grid Filter Cleared")
        msg.setText("Grid Filter has been cleared, please reload display")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()  # this will show our messagebox
        self.stateslabel.setText("All Grids Shown")
        self.stateclear.hide()




    def loadData(self):
        #print("\n load data restarted")

        self.readconfig()
        global statelist
        global start
        print(start)

        global end
        print(end)
        global selectedgroup
        global loadflag
        if loadflag < 1:
            #start = (self.start_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))
            #end = (self.end_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))

            print("launching default SR Report Display")
            loadflag = 1
            #start = (self.start_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))
            #end = (self.end_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))
        else:
            start = (self.start_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))
            end = (self.end_datetime.dateTime().toString("yyyy-MM-dd HH:mm"))





        if self.green.isChecked() == True:
            green = "1"
        else:
            green = "5"
        if self.yellow.isChecked() == True:
            yellow = "2"
        else:
            yellow = "5"

        if self.red.isChecked() == True:
            red = "3"
        else:
            red = "5"

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
        header.setStretchLastSection(True)
        # header.horizontalHeaderStretchLastSection = True
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.sortItems(0, QtCore.Qt.DescendingOrder)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 9)
        #print("loadData completed \n \n")
        #self.filetest()
        connection.close()
        self.mapperWidget()




    def mapperWidget(self):
        global mapper
        global data
        global map_flag
        global start
        global end
        global selectedgroup
        global statelist




        gridlist = []


        self.mapwidget.deleteLater()
        self.mapwidget = QWebEngineView()
        self.mapwidget.setObjectName("widget")

        if self.green.isChecked() == True:
            green = 1
        else:
            green = 0
        if self.yellow.isChecked() == True:
            yellow = 2
        else:
            yellow = 0

        if self.red.isChecked() == True:
            red = 3
        else:
            red = 0
        ##################################




        mapper = QWebEngineView()
        coordinate = (38.8199286, -90.4782551)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate

        )

        try:
            connection = sqlite3.connect('traffic.db3')
            #cur = connection.cursor()

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
                print(call + " before lat  & Long " + str(testlat) + "  " + str(testlong))
                if count > 0:
                    print("latbefore :"+str(testlat))
                    testlat = testlat + (count * .010)
                    print("latafter :" + str(testlat))
                    testlong = testlong +(count * .010)
                gridlist.append(grid)
                print(call+" After lat  & Long "+str(testlat)+"  "+str(testlong))
                testlat = float(testlat)
                testlong = float(testlong)







                #glat = gridLatint
                #glon = gridLongint
                glat = testlat
                glon = testlong






            #query = "SELECT gridlat, gridlong, callsign, date  FROM checkins_Data where groupname = ? and date like ? or date LIKE ?"
            #cursor.execute(query, (selectedgroup, '%' + todaystring2 + '%', '%' + yesterday + '%'))


            #sqlite_select_query = 'SELECT gridlat, gridlong, callsign, date FROM checkins_Data where groupname=?'
            #cursor.execute(sqlite_select_query, (selectedgroup,))
            #tems = cursor.fetchall()

            #for item in items:
            #    glat = item[0]
            #    glon = item[1]
            #    call = item[2]
            #    ack = item[3]
            #    utc = item[4]




                pinstring = ("Callsign :")
                html = '''<HTML> <BODY><p style="color:blue;font-size:14px;">%s %s<br>
                StatRep ID :
                %s  
                </p></BODY></HTML>''' % (pinstring,call,srid,)
                iframe = folium.IFrame(html,
                                       width=160,
                                       height=70)

                popup = folium.Popup(iframe,
                                     min_width=100, max_width=160)
                #folium.Marker(location=[glat, glon], popup=popup).add_to(m)
                #print(status)
                if "2" in status and yellow == 2:
                    color = "orange"
                    radius = 40
                    filler = True
                elif "2" in status and yellow == 0:
                    color = ""
                    radius = 40
                    filler = False

                elif "3" in status and red == 3:
                    color = "red"
                    radius = 40
                    filler = True
                elif "3" in status and red == 0:
                    color = ""
                    radius = 40
                    filler = False

                elif "1" in status and green == 1:
                        color = "green"
                        radius = 6
                        filler = True
                elif "1" in status and green == 0:
                        color = ""
                        radius = 6
                        filler = False



                folium.CircleMarker(radius=radius,fill=filler, color=color, fill_color=color,

                 location=[glat, glon], popup=popup, icon=folium.Icon(color="red")).add_to(m)


            #cur.close()
            #cursor.close()

        except sqlite3.Error as error:
            print("Data Manager Failed to read data from sqlite table", error)
        finally:
            if (connection):
                connection.close()

         #       print("The SQLite connection is closed")
        # return map

        # folium.Marker(location=[38.655800, -87.274721],popup='<h3 style="color:green;">Marker2</h3>').add_to(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        m.save('map.html')
        #self.build_report()

        #mapper.setHtml(data.getvalue().decode())

       # if map_flag == 1:
            #mapper.closeEvent()
            #self.widget.deleteLater()
            #self.widget = QWebEngineView()
            #self.widget.setObjectName("widget")
        #    mapper.setHtml(data.getvalue().decode())
        #    mapper.reload()
            #self.gridLayout_2.addWidget(mapper, 4, 0, 2, 5)
         #   print("\n \n executed map reload \n \n")

        #else:
        #    mapper.setHtml(data.getvalue().decode())
            #self.widget.setHtml(data.getvalue().decode())
        #    self.gridLayout_2.addWidget(mapper, 4, 0, 2, 5)
        #    map_flag = 1
        #    print("\n \n Executed map update \n \n")
        #mapper.deleteLater()

        self.mapwidget.setHtml(data.getvalue().decode())
        #self.mapwidget.show()
        #print(self.mapwidget.show())
        self.layout.addWidget(self.mapwidget, 4, 0, 1, 9)

        #print("added widget")
        #self.buildreport()



    def buildreport(self):
        global start
        global end
        global selectedgroup
        global rname

        with open(r'map.html', 'r') as fp:
            # read all lines using readline()
            lines = fp.readlines()
            for row in lines:
                # check if string present on a current line
                word = 'position: relative;'
                # print(row.find(word))
                # find() method returns -1 if the value is not found,
                # if found it returns index of the first occurrence of the substring
                if row.find(word) != -1:
                    print('string exists in file')
                    print('line Number:', lines.index(row))
                    startline = (lines.index(row))
                    linea = startline + 1
                    lineb = startline + 2
                    linec = startline + 3

        with open('map.html', 'r', encoding='utf-8') as file:
            data = file.readlines()



        #print(data)
        data[linea] = "                    width: 75.0%;\n"
        data[lineb] = "                    height: 60.0%;\n"
        data[linec] = "                    left: 12.5%;\n"

        with open('map.html', 'w', encoding='utf-8') as file:
            file.writelines(data)



        if self.green.isChecked() == True:
            green = "1"
        else:
            green = "5"
        if self.yellow.isChecked() == True:
            yellow = "2"
        else:
            yellow = "5"

        if self.red.isChecked() == True:
            red = "3"
        else:
            red = "5"




        #conn = sqlite3.connect('traffic.db3')
        #query = ("SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments FROM StatRep_Data WHERE groupname = ? AND datetime BETWEEN ? AND ? AND status = ? OR status = ? OR status = ?")
        #result = conn.execute(query, (selectedgroup, start, end, red, yellow, green))

        #cursor = conn.cursor()
        #cursor.execute(query, (selectedgroup, start, end, red, yellow, green))
        #result = cursor.fetchall()


        connection = sqlite3.connect('traffic.db3')
        cursor = connection.cursor()

        query = ("SELECT datetime, SRid, callsign, grid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, political, comments "
                 "FROM StatRep_Data WHERE groupname = ? AND (status  = ? OR status = ? OR status = ?) AND datetime BETWEEN ? AND ? AND substr(grid,1,2) IN ({})".format(', '.join('?' for _ in statelist)))
        result = cursor.execute(query, [selectedgroup, green, yellow, red, start, end] +statelist)





        rname1 = format(self.report_name.text())
        rname = re.sub('[^0-9a-zA-Z]+', '_', rname1)
        #rname = re.sub("[^A-Za-z0-9*\-\s]+", " ", rname1)

        if len(rname) < 2:
            msg = QMessageBox()
            msg.setWindowTitle("CommStat Report Name Error")
            msg.setText("Commstat Report name too short")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            x = msg.exec_()  # this will show our messagebox
            return
        else:
            os.rename('map.html', rname+'.html')
            newname = rname+".html"


        html = "<html><title>&nbsp; Commstat Status Report Data to HTML</title><body><STYLE TYPE='text/CSS'><!--/* The margin order is: top right bottom left */" \
                                                                                                          "BODY { margin: 0 auto;" \
                                                                                                          "font-family: Helvetica, Times, Geneva;" \
                                                                                                          "font-size: 10pt;" \
                                                                                                          "font-style: plain" \
                                                                                                          "text-align: center;" \
                                                                                                          "background-color: white;" \
                                                                                                          "}" \
               "</STYLE>" \
               "<p style=text-align:center><br>&nbsp;&nbsp; <b>Report name :</b> &nbsp;"+newname+"&nbsp;&nbsp;&nbsp;&nbsp; <b>Report Start Date / Time :</b>&nbsp;"+start+"&nbsp;&nbsp;&nbsp;&nbsp; <b>Report End Date Time :</b>&nbsp;"+end+"<br></p>" \
                                                                                                                                                                  "<table style ='width :75%' > <style> table, th, td {  border: 2px solid; margin: 0px auto;} </style> <tr><td><b> &nbsp;&nbsp;Date Time UTC </b></td><td><b>&nbsp; ID &nbsp;</b></td><td><b>&nbsp; Callsign</b></td><td><b>&nbsp;Grid&nbsp;</b></td><td><b>&nbsp; Priority &nbsp;</b></td><td><b> &nbsp; Stat &nbsp; </b></td><td><b>&nbsp;Pow </b>&nbsp; </td><td><b>&nbsp; H20 &nbsp;</b></td><td><b>&nbsp; Med&nbsp; </b></td><td><b>&nbsp; Com &nbsp; </b></td><td><b>&nbsp; Trv &nbsp;</b></td><td><b>&nbsp; Int &nbsp;</b> </td><td><b>&nbsp;Fuel &nbsp;</b></td><td><b>&nbsp; Food &nbsp;</b></td><td><b>&nbsp; Cri &nbsp;</b></td><td><b>&nbsp; Civ &nbsp; </b></td><td><b>&nbsp;Pol &nbsp;</b></td><td><b>&nbsp; Remarks &nbsp; </b></td></tr>"



        color1 = "green"
        color2 = "yellow"
        color3 = "red"
        for row in result:
            srdatetime = row[0]
            srstatus = row[5]
            srpow = row[6]
            srh20 = row[7]
            srmed = row[8]
            srota = row[9]
            srtrav = row[10]
            srnet = row[11]
            srfuel = row[12]
            srfood = row[13]
            srcrime = row[14]
            srcivil = row[15]
            srpolitical = row[16]


            if "1" in srstatus:
                colorsr5 = color1
            if "2" in srstatus:
                    colorsr5 = color2
            if "3" in srstatus:
                colorsr5 = color3
            if "1" in srpow:
                colorsr6 = color1
            if "2" in srpow:
                    colorsr6 = color2
            if "3" in srpow:
                colorsr6 = color3


            if "1" in srh20:
                colorsr7 = color1
            if "2" in srh20:
                    colorsr7 = color2
            if "3" in srh20:
                colorsr7 = color3

            if "1" in srmed:
                colorsr8 = color1
            if "2" in srmed:
                    colorsr8 = color2
            if "3" in srmed:
                colorsr8 = color3

            if "1" in srota:
                colorsr9 = color1
            if "2" in srota:
                    colorsr9 = color2
            if "3" in srota:
                colorsr9 = color3

            if "1" in srtrav:
                colorsr10 = color1
            if "2" in srtrav:
                    colorsr10 = color2
            if "3" in srtrav:
                colorsr10 = color3

            if "1" in srnet:
                colorsr11 = color1
            if "2" in srnet:
                    colorsr11 = color2
            if "3" in srnet:
                colorsr11 = color3

            if "1" in srfuel:
                colorsr12 = color1
            if "2" in srfuel:
                    colorsr12 = color2
            if "3" in srfuel:
                colorsr12 = color3

            if "1" in srfood:
                colorsr13 = color1
            if "2" in srfood:
                    colorsr13 = color2
            if "3" in srfood:
                colorsr13 = color3

            if "1" in srcrime:
                colorsr14 = color1
            if "2" in srcrime:
                    colorsr14 = color2
            if "3" in srcrime:
                colorsr14 = color3

            if "1" in srcivil:
                colorsr15 = color1
            if "2" in srcivil:
                    colorsr15 = color2
            if "3" in srcivil:
                colorsr15 = color3

            if "1" in srpolitical:
                colorsr16 = color1
            if "2" in srpolitical:
                    colorsr16 = color2
            if "3" in srpolitical:
                colorsr16 = color3


            html += "<tr><td>"
            html += "&nbsp; " +str(srdatetime)+" &nbsp; &nbsp;</td><td> &nbsp; &nbsp;"+row[1]+" &nbsp;&nbsp;</td><td>"+row[2]+" &nbsp;&nbsp; </td><td> &nbsp;&nbsp; "+row[3]+" &nbsp;&nbsp; </td><td>&nbsp;&nbsp;  "+row[4]+"&nbsp;&nbsp;</td><td style = background-color:"+colorsr5+";><font color = "+colorsr5+">&nbsp;"+row[5]+"&nbsp;</td><td style = background-color:"+colorsr6+";><font color = "+colorsr6+">&nbsp;"+row[6]+"&nbsp;</td><td style = background-color:"+colorsr7+";><font color = "+colorsr7+">&nbsp;"+row[7]+"&nbsp;</td><td style = background-color:"+colorsr8+";><font color = "+colorsr8+">&nbsp;"+row[8]+"&nbsp;</td><td style = background-color:"+colorsr9+";><font color = "+colorsr9+">&nbsp;"+row[9]+"&nbsp;</td><td style = background-color:"+colorsr10+";><font color = "+colorsr10+">&nbsp;"+row[10]+"&nbsp;</td><td style = background-color:"+colorsr11+";><font color = "+colorsr11+">&nbsp;"+row[11]+"&nbsp;</td><td style = background-color:"+colorsr12+";><font color = "+colorsr12+">&nbsp;"+row[12]+"&nbsp;</td><td style = background-color:"+colorsr13+";><font color = "+colorsr13+">&nbsp;"+row[13]+"&nbsp;</td><td style = background-color:"+colorsr14+";><font color = "+colorsr14+">&nbsp;"+row[14]+"&nbsp;</td><td style = background-color:"+colorsr15+";><font color = "+colorsr15+">&nbsp;"+row[15]+"&nbsp;</td><td style = background-color:"+colorsr16+";><font color = "+colorsr16+">&nbsp;"+row[16]+"&nbsp;</td><td>&nbsp;&nbsp;"+row[17]
            html += "</tr></td>"
        html += "</table></body></html>"
        file = open(newname, "a")
        file.write(html)
        file.close()
        path = os.path.join('reports', newname)
        os.replace(newname, path)


        msg = QMessageBox()
        msg.setWindowTitle("CommStat Report Created ")
        msg.setText("CommStat Report : "+rname+"  Created  & placed in reports folder")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        x = msg.exec_()  # this will show our messagebox
        return



app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

