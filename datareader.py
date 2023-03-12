import os.path
from configparser import ConfigParser
import js8callAPIsupport
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime, Qt
import shutil
import numpy as np
import re
import sqlite3
from datetime import datetime, timedelta
import time
import psutil
import platform
import maidenhead as mh
import subprocess
import sys
os.system('')
OS_Directed =""

def getConfig():
    if os.path.exists("config.ini"):
        global callsign
        global callsignSuffix
        global group1
        global group2
        global grid
        global path
        global selectedgroup
        config_object = ConfigParser()
        config_object.read("config.ini")
        userinfo = config_object["USERINFO"]
        # print("callsign is {}".format(userinfo["callsign"]))
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
        if len(group2) < 4:
            group2 = group1
        grid = format(userinfo["grid"])
        path = format(systeminfo["path"])
        selectedgroup = format(userinfo["selectedgroup"])
        

    else:
        msg = QMessageBox()
        msg.setWindowTitle("CommStatX error")
        msg.setText("Config file is missing!")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()  # this will show our messagebox
        return

def oscheck():
    global OS
    global bull1
    global bull2
    global OS_Directed
    pios = "aarch64"
    winos = "Windows"
    linuxos = "Linux"
    if pios in (platform.platform()):
        print("Datareader this is Pi 64bit OS")
        OS = "pi"
        bull1 = 0
        bull2 = 4
    if winos in (platform.platform()):
        print("Datareader this is Windows OS")
        OS_Directed = "\DIRECTED.TXT"
        # sudo apt install ./python-pyqt5.qtwebengine_5.15.2-2_arm64.deb
    if linuxos in (platform.platform()):
        print("Datareader this is Linux OS")
        OS_Directed = "/DIRECTED.TXT"

    else:
        # print("This is not 64bit PiOS")
        # OS = "Mint"
        print("Datareader Operating System is :" + platform.platform())
        print("Datareader Python version is :" + platform.python_version())
oscheck()
getConfig()




def copyDirected():
    global OS_Directed
    filepath = path+""+OS_Directed
    shutil.copy2(filepath, 'copyDIRECTED.TXT')  # complete target filename given
    #shutil.copy2('/src/file.ext', '/dst/dir')  # target filename is /dst/dir/file.ext
#copyDirected()









def prGreen(prt):
        print(f"\033[92m{prt}\033[00m")
        
def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")
    
def prRed(prt):
    print(f"\033[91m{prt}\033[00m")




def parseDirected():
    global group1
    global group2
    membergrp1 = ""
    membergrp2 = ""
    global selectedgroup

    conn = sqlite3.connect("traffic.db3")
    cur = conn.cursor()
    datafile = open("copyDIRECTED.TXT", "r")
    lines = datafile.readlines()
    last_lines = lines[-50:]
    for num, str1 in enumerate(last_lines, 1):
        try:
            if selectedgroup in str1:
                currentgrp = selectedgroup
                #print("group1 is in string : "+currentgrp)
                membergrp1 = group1
                membergrp2 = group2
            
            #if group2 in str1:
            #    currentgrp = group2
            #    membergrp2 = group2
            #    print("group2 is in string : " +currentgrp)
            


            #if  group1 or group2 in currentgrp:

                if "{^%}" in str1: #THIS IS BULLETINS
                    #arr = line.split('\t')
                     #str1.replace('\t', ', ')
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    if count != 9:
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    bulletin = arr2[2]
                    #print(currentgrp)
                    #print(arr)

                    cur.execute("INSERT OR REPLACE INTO bulletins_Data (datetime, idnum, groupid, callsign, message) VALUES(?, ?, ?, ?, ? )", (utc, id, currentgrp, callsign, bulletin))
                    conn.commit()
                    
                    prGreen(str1.rstrip())
                    prGreen ("Added Bulletin from :"+callsign+" ID :"+id)
                    prYellow("Attempting to add callsign :"+callsign+" to members list")

                    continue

                #forwarded statrep
                ###
                if "{F%}" in str1:  # THIS IS A Forwarded STATREP
                    mylist = ['1', '2', '3', '4']
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    # print (count)
                    if count != 13:
                        prRed("StatRep forwarded message failed field count, missing fields \n" + str1 + " \n \n")
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    curgrid = arr2[1]
                    prec1 = arr2[2]
                    orig_call = arr2[6]
                    #print(orig_call)
                    if prec1 == "1":
                        prec = "Routine"

                    if prec1 == "2":
                        prec = "Priority"

                    if prec1 == "3":
                        prec = "Immediate"

                    if prec1 == "4":
                        prec = "Flash"
                    # for item in mylist:
                    #    if item in prec1:
                    #        print("StatRep failed for null precedence field :"+str1)
                    #        continue
                    #   else:
                    #      print("here is the else statement")

                    if prec1 not in ["1", "2", "3", "4"]:
                        prRed("Forwarded StatRep failed for null precedence field :" + str1 + " \n \n")
                        continue

                    srid = arr2[3]

                    srcode = arr2[4]
                    arr5 = list(srcode)
                    status = arr5[0]
                    if status not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null status field :" + str1 + " \n \n")
                        continue
                    commpwr = arr5[1]
                    if commpwr not in ["1", "2", "3"]:
                        print("Forwarded StatRep failed for null commpwr field :" + str1 + " \n \n")
                        continue
                    pubwtr = arr5[2]
                    if pubwtr not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null pubwtr field :" + str1 + " \n \n")
                        continue
                    med = arr5[3]
                    if med not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null med field :" + str1 + " \n \n")
                        continue
                    ota = arr5[4]
                    if ota not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null ota field :" + str1 + " \n \n")
                        continue
                    trav = arr5[5]
                    if trav not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null trav field :" + str1 + " \n \n")
                        continue
                    net = arr5[6]
                    if net not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null net field :" + str1 + " \n \n")
                        continue
                    fuel = arr5[7]
                    if fuel not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null fuel field :" + str1 + " \n \n")
                        continue
                    food = arr5[8]
                    if food not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null food field :" + str1 + " \n \n")
                        continue
                    crime = arr5[9]
                    if crime not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null crime field :" + str1 + " \n \n")
                        continue
                    civil = arr5[10]
                    if civil not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null or missing civil field :" + str1 + " \n \n")
                        continue
                    pol = arr5[11]
                    if pol not in ["1", "2", "3"]:
                        prRed("Forwarded StatRep failed for null pol field :" + str1 + " \n \n")
                        continue


                    comments = arr2[5]
                    cur.execute(
                        "INSERT OR REPLACE INTO Statrep_Data (datetime, callsign, groupname, grid, SRid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel , food, crime, civil, political, comments) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ? )",
                        (utc, orig_call, currentgrp, curgrid, srid, prec, status, commpwr, pubwtr, med, ota, trav, net,
                         fuel, food, crime, civil, pol, comments))
                    conn.commit()
                    # print(arr2)
                    prGreen(str1.rstrip())
                    prGreen("Added StatRep from :" + orig_call + " ID :" + srid)
                    #prYellow("Attempting to add or update callsign :" + orig_call + " to members list")

                    continue



                #original Statrep
                if "{&%}" in str1: #THIS IS STATREP
                    mylist = ['1','2','3','4']
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    #print (count)
                    if count != 12:
                        prRed("StatRep message failed field count, missing fields \n"+str1+" \n \n")
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    curgrid = arr2[1]
                    prec1 = arr2[2]
                    if prec1 == "1":
                        prec = "Routine"

                    if prec1 == "2":
                        prec = "Priority"

                    if prec1 == "3":
                        prec = "Immediate"

                    if prec1 == "4":
                        prec = "Flash"
                    #for item in mylist:
                    #    if item in prec1:
                    #        print("StatRep failed for null precedence field :"+str1)
                    #        continue
                     #   else:
                      #      print("here is the else statement")
                      
                    if prec1 not in ["1","2","3","4"] :
                        prRed("StatRep failed for null precedence field :"+str1+" \n \n")
                        continue
                    
                    srid = arr2[3]
                    
                    srcode = arr2[4]
                    arr5 = list(srcode)
                    status = arr5[0]
                    if status not in ["1","2","3"] :
                        prRed("StatRep failed for null status field :"+str1+" \n \n")
                        continue
                    commpwr = arr5[1]
                    if commpwr not in ["1","2","3"]:
                        print("StatRep failed for null commpwr field :"+str1+" \n \n")
                        continue
                    pubwtr = arr5[2]
                    if pubwtr not in ["1","2","3"]:
                        prRed("StatRep failed for null pubwtr field :"+str1+" \n \n")
                        continue
                    med = arr5[3]
                    if med not in ["1","2","3"]:
                        prRed("StatRep failed for null med field :"+str1+" \n \n")
                        continue
                    ota = arr5[4]
                    if ota not in ["1","2","3"]:
                        prRed("StatRep failed for null ota field :"+str1+" \n \n")
                        continue
                    trav = arr5[5]
                    if trav not in["1","2","3"] :
                        prRed("StatRep failed for null trav field :"+str1+" \n \n")
                        continue
                    net = arr5[6]
                    if net not in ["1","2","3"]:
                        prRed("StatRep failed for null net field :"+str1+" \n \n")
                        continue
                    fuel = arr5[7]
                    if fuel not in ["1","2","3"]:
                        prRed("StatRep failed for null fuel field :"+str1+" \n \n")
                        continue
                    food = arr5[8]
                    if food not in ["1","2","3"]:
                        prRed("StatRep failed for null food field :"+str1+" \n \n")
                        continue
                    crime = arr5[9]
                    if crime not in ["1","2","3"] :
                        prRed("StatRep failed for null crime field :"+str1+" \n \n")
                        continue
                    civil = arr5[10]
                    if civil not in ["1","2","3"]:
                        prRed("StatRep failed for null or missing civil field :"+str1+" \n \n")
                        continue
                    pol = arr5[11]
                    if pol not in ["1","2","3"]:
                        prRed("StatRep failed for null pol field :"+str1+" \n \n")
                        continue
                        
                    comments = arr2[5]
                    cur.execute("INSERT OR REPLACE INTO Statrep_Data (datetime, callsign, groupname, grid, SRid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel , food, crime, civil, political, comments) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (utc, callsign, currentgrp, curgrid, srid, prec, status, commpwr, pubwtr, med, ota, trav, net, fuel, food, crime, civil, pol, comments))
                    conn.commit()
                    #print(arr2)
                    prGreen(str1.rstrip())
                    prGreen ("Added StatRep from :"+callsign+" ID :"+srid)
                    #prYellow("Attempting to add or update callsign :"+callsign+" to members list")

                    continue
                if "{*%}" in str1:  #THIS IS MARQUEE
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    if count != 10:
                        continue
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    color = arr2[2]
                    marquee = arr2[3]
                    prYellow("Received marquee to be written - id :"+id+" callsign :"+callsign+" groupname :"+currentgrp+" time :"+utc+" color :"+color+" mesaage : "+marquee)
                    cur.execute("INSERT OR REPLACE INTO marquees_Data (idnum, callsign, groupname, date, color, message) VALUES(?, ?, ?, ?, ?, ?)", (id, callsign, currentgrp, utc, color, marquee))
                    conn.commit()
                    
                    #print(count)
                    prGreen(str1.rstrip()) 
                    prGreen("Added Marquee from :"+callsign+" ID :"+id)
                    #prYellow("Attempting to add or update callsign "+callsign+" in members list")

                    continue

                if "CS?" in str1:  # THIS IS CS RESPONSE

                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    #print(str(count))
                    if count != 6:
                        continue
                    #id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]
                    #color = arr2[2]
                    #marquee = arr2[3]
                    prYellow("Received CS Request to be responsed to - from "+callsign)
                    subprocess.run([sys.executable, "csresponder.py" , utc])





                    #prGreen("Transmitted CS1 Capable")

                    # prYellow("Attempting to add or update callsign "+callsign+" in members list")

                    continue
                
                
                if "{~%}" in str1:  # THIS IS CHECKIN
                    gridlist = []
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    count = len(arr) + len(arr2)
                    countstr1 = (str(count))
                    if count != 10:
                        prRed(str1.rstrip())
                        prRed("Check in field count :"+countstr1+" 10 fields required, Commstatx cannot process this check in \n \n")
                        continue
                    #prGreen("checkin count is equal to 8 "+(countstr1)+" \n \n")
                    id = arr2[1]
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]

                    traffic = arr2[1]
                    state = arr2[2]
                    grid = arr2[3]
                    if len(grid) == 6:
                        coords = mh.to_location(grid)
                        #print("6 digit")
                    else:
                        coords = mh.to_location(grid, center=True)
                    #print(state,grid)
                    #coords = mh.to_location(grid, center=True)
                    testlat = float(coords[0])
                    testlong = float(coords[1])

                    count = gridlist.count(grid)
                    #print(callsign + " before lat  & Long " + str(testlat) + "  " + str(testlong))
                    #if count > 0:
                    #    print("latbefore :" + str(testlat))
                    #    testlat =  100.00
                    #
                    #    print("latafter :" + str(testlat))
                    #    testlong = testlong + (count * .010)
                    #gridlist.append(grid)
                    #print(callsign + " After lat  & Long " + str(testlat) + "  " + str(testlong))
                    #testlat = float(testlat)
                    #testlong = float(testlong)



                    conn5 = sqlite3.connect("traffic.db3")
                    cur5 = conn5.cursor()
                    rowsQuery = "SELECT Count() FROM members_Data Where grid  = '" + grid + "'"
                    cur5.execute(rowsQuery)
                    numberOfRows = cur5.fetchone()[0]
                    if numberOfRows > 1:
                        print("latbefore :" + str(testlat))
                        testlat = testlat + (numberOfRows * .010)
                        #print("latafter :" + str(testlat))
                        testlong = testlong + (numberOfRows * .010)

                    conn0 = sqlite3.connect("traffic.db3")
                    cur0 = conn0.cursor()
                    cur0.execute(
                        "INSERT OR REPLACE INTO members_Data (date, callsign, groupname1, groupname2, gridlat, gridlong, state, grid) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        (utc, callsign, membergrp1, membergrp2, testlat, testlong, state, grid))
                    conn0.commit()
                    cur0.close()
                    #print(str(numberOfRows))

                        # print(lastheard, call, gridLat, gridLong)
                    conn2 = sqlite3.connect("traffic.db3")
                    cur2 = conn2.cursor()
                    cur2.execute(
                        "INSERT OR IGNORE INTO checkins_Data (date, callsign, groupname, traffic, gridlat, gridlong, state, grid) VALUES(?, ?, ?, ?, ? , ? , ? , ? )",
                          (utc,callsign, currentgrp, traffic, testlat, testlong, state, grid))
                    conn2.commit()
                    cur2.close()
                    prGreen(str1.rstrip())
                    prGreen("Added Check in from callsign :"+callsign)
                    prYellow("Attempting to add or update callsign to members list")

                    continue

                    #else:
                    #    prRed(str1.rstrip())
                    #    prRed("Found callsign:"+callsign+" Found group :"+currentgrp+ " failed parse criteria, or not callsign in database, unable to add msg to database")
                    #    prYellow("Attempting to add or update callsign :"+callsign+" to members list")
                    #
                    #    continue
                    
                else:
                    #prYellow("Message failed Commstatx msg criteria attempting to add to member list, current group :"+currentgrp)
                    try:
                        arr = str1.split('\t')
                        utc = arr[0]
                        callsignmix = arr[4]
                        arr2 = callsignmix.split(',')
                        callsignlong = arr2[0]
                        arr3 = callsignlong.split(':')
                        callsignlg = arr3[0]
                        arr4 = callsignlg.split('/')
                        callsign = arr4[0]
                        if len(callsign) > 3 and len(callsign) < 7:
                            #getheard(callsign, utc)
                            prRed (str1.rstrip())
                            prRed("Failed Commstatx criteria, probably not a Commstatx msg")
                            #prGreen("Added :"+callsign+" to heard list ")
                            #prYellow("Attempting to update Members List for Callsign "+callsign)

                                
                        else:
                            prRed(str1.rstrip())
                            prRed("Failed callsign structure criteria, msg not parsed into database \n \n")
                            continue
                        
                    except IndexError:
                        prRed(str1.rstrip())
                        prRed(callsign+"Failed Commstatx index criteria, probably not a Commstatx msg not parsed into database")
                        continue
                    

                    
            else:
                #print("No group found in string, attempting to add to heard list :")
                try:
                    #print("An exception occurred")
                    arr = str1.split('\t')
                    utc = arr[0]
                    callsignmix = arr[4]
                    arr2 = callsignmix.split(',')
                    callsignlong = arr2[0]
                    arr3 = callsignlong.split(':')
                    callsignlg = arr3[0]
                    arr4 = callsignlg.split('/')
                    callsign = arr4[0]

                    
                    if len(callsign) > 3 and len(callsign) < 7:

                        prRed(str1.rstrip())
                        prRed("Failed Commstatx msg criteria, incorrect group or possibly not a Commstatx msg ")
                        #prGreen("Added :"+callsign+" to heard list ")
                        #prYellow("Testing to see if callsign is in Members List")
                        #test_member(callsign, membergrp1,membergrp2, utc)
                        
                        
                        #prYellow("Attempting to update Members List for Callsign "+callsign)

                                
                    else:
                        prRed(str1.rstrip())
                        prRed("Failed callsign structure criteria, msg not parsed into database \n \n")
                        continue
                except:
                        print(str1)
                        print("An exception occurred with the above string, nothing could be done with this")





                    #cur.execute("INSERT OR REPLACE INTO checkins_Data (date, callsign, groupname, traffic) VALUES(?, ?, ?, ?)",(utc, callsign, currentgrp, traffic))
                    #conn.commit()

                    #print(arr2[1])

        except IndexError:
            prRed(str1.rstrip())
            print("Received string failed index criteria, msg not parsed into database \n \n")
            continue


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


copyDirected()
parseDirected()
now = QDateTime.currentDateTime()
now = (now.toUTC().toString("yyyy-MM-dd HH:mm:ss"))


#now = datetime.now()
print("Datareader stopped :"+now)



def runreaders():
    while True:
        getConfig()
        copyDirected()
        parseDirected()
        now = datetime.now()
        print(now)
        if checkIfProcessRunning('SQLiteSpy.exe'):
            print('Yes CommStatX is still running')
        else:
            print( 'CommStatX has stopped')
            quit()
            #import sys
            #sys.exit()
        #time.sleep(30)


#runreaders()

