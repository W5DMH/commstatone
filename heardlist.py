import os
import sqlite3
from configparser import ConfigParser
import re
from time import strftime
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import datetime
import js8callAPIsupport
import folium
import sqlite3
import io


serverip = ""
serverport = ""
callsign = ""
grid = ""
selectedgroup = ""
mapper = ""

class Ui_FormHeard(object):
    def setupUi(self, FormHeard):
        FormHeard.setObjectName("FormHeard")
        FormHeard.resize(950, 678)
        font = QtGui.QFont()
        font.setPointSize(10)
        FormHeard.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("USA-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FormHeard.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(FormHeard)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(FormHeard)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 3, 1, 1, QtCore.Qt.AlignRight)
        self.tableWidget = QtWidgets.QTableWidget(FormHeard)
        self.tableWidget.setObjectName("tableWidget")
        #self.tableWidget.setColumnCount(0)
        #self.tableWidget.setRowCount(0)
        #self.gridLayout.addWidget(self.tableWidget, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(FormHeard)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.getConfig()
        self.loadheard()
        self.mapperWidget()

        self.retranslateUi(FormHeard)
        QtCore.QMetaObject.connectSlotsByName(FormHeard)

    def retranslateUi(self, FormHeard):
        _translate = QtCore.QCoreApplication.translate
        FormHeard.setWindowTitle(_translate("FormHeard", "CommStat Heard List"))
        #self.label.setText(_translate("FormHeard", "TextLabel"))


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
            print(labeltext)
            self.label.setText("net tezt here")
            #self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
            self.label.setText( labeltext)






    def mapperWidget(self):
        global mapper
        mapper = QWebEngineView()
        coordinate = (38.8199286, -90.4782551)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=4,
            location=coordinate

        )

        try:
            sqliteConnection = sqlite3.connect('traffic.db3')
            cursor = sqliteConnection.cursor()

            #query = "SELECT datetime, idnum, callsign, message FROM bulletins_Data where groupid = ?"
           # result = connection.execute(query, (selectedgroup,))

            sqlite_select_query = 'SELECT gridlat, gridlong, callsign, date FROM heard_Data'
            cursor.execute(sqlite_select_query)
            items = cursor.fetchall()

            for item in items:
                glat = item[0]
                glon = item[1]
                call = item[2]
                utc = item[3]

                pinstring = (" Last Heard :")
                html = '''<HTML> <BODY><p style="color:blue;font-size:14px;">%s<br>
                %s<br>
                %s
                </p></BODY></HTML>''' % (call, pinstring, utc)
                iframe = folium.IFrame(html,
                                       width=160,
                                       height=70)

                popup = folium.Popup(iframe,
                                     min_width=100, max_width=160)
                #folium.Marker(location=[glat, glon], popup=popup).add_to(m)
                folium.CircleMarker(radius=6,fill=True, fill_color="darkblue",
                 location=[glat, glon], popup=popup, icon=folium.Icon(color="red")).add_to(m)


            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (sqliteConnection):
                sqliteConnection.close()
         #       print("The SQLite connection is closed")
        # return map

        # folium.Marker(location=[38.655800, -87.274721],popup='<h3 style="color:green;">Marker2</h3>').add_to(m)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        #self.gridLayout.addWidget()widget = QWebEngineView()
        mapper.setHtml(data.getvalue().decode())
        self.gridLayout_2.addWidget(mapper, 2, 0, 1, 2)
        #print("Mapping completed")
        self.loadheard()
        #QtCore.QTimer.singleShot(90000, self.mapperWidget)
        #QtCore.QTimer.singleShot(90000, self.run_mapper)

    def run_mapper(self):
        global mapper
        mapper.deleteLater()
        print("stopped previous map")
        self.mapperWidget()

    def loadheard(self):
        #self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        connection = sqlite3.connect('traffic.db3')
        query = "SELECT date, callsign FROM heard_Data"
        result = connection.execute(query)

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        table = self.tableWidget
        table.setHorizontalHeaderLabels(
            str("Date Time UTC ;Callsign").split(
                ";"))
        header = table.horizontalHeader()
        header.resizeSection(0, 220)
        header.resizeSection(1, 220)
        #header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #header.setStretchLastSection(True)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # self.tableWidget = QtWidgets.QTableWidget()
        # self.addWidget(QTableWidget(table),0, 0, 1, 2)
        # self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.sortItems(0, QtCore.Qt.DescendingOrder)
        self.gridLayout.addWidget(self.tableWidget, 2, 1, 1, 3)

        #print("Load Bulletins & Marquee Completed")
        #QtCore.QTimer.singleShot(30000, self.loadbulletins)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FormHeard = QtWidgets.QWidget()
    ui = Ui_FormHeard()
    ui.setupUi(FormHeard)
    FormHeard.show()
    sys.exit(app.exec_())
