#!/usr/bin/env python3
import subprocess
import sys
import os
import platform

pyver = ""

osver = ""


def oscheck():
    global OS
    global bull1
    global bull2
    global osver
    pios = "aarch64"
    lin = "Linux"
    win = "Windows"
    if pios in (platform.platform()):
        print("This is Pi 64bit OS")
        osver = "pi"
        bull1 = 0
        bull2 = 4
        osver = lin
        test_python()
    # sudo apt install ./python-pyqt5.qtwebengine_5.15.2-2_arm64.deb

    elif lin in (platform.platform()):
        osver = lin
        with open('/etc/issue') as f:
            first_line = f.readline()
            f.close
        if "21" or "20" in first_line:
            print("here is the first line :" + first_line)
            test_python()
    elif win in (platform.platform()):
        print("This is Windows")
        osver = win
        test_python()
    else:
        print("Commstat does not recognize this operating system and cannot proceed.")
        return


def runsettings():
    subprocess.call([sys.executable, "settings.py"])


def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    except subprocess.CalledProcessError as e:
        # print("this is the except install error: "+str(e.returncode))
        if e.returncode > 0:
            print(
                " Installation failed, copy and paste this screen \n into https://groups.io/g/CommStat for support exiting now")
            sys.exit()
            # Exception("failed installation, cannot conntinue")


def test_python():
    global osver
    print("HERE is the version "+osver)
    try:
        if int(sys.version_info[0]) < 3:
            print("You are using Python " + str(sys.version_info[0]))
            print("Commstatx requires Python 3.9 or newer, install cannot continue")
            # raise Exception("Wrong Python version, cannot continue installation, please upgrade Python")
            sys.exit()

        if int(sys.version_info[1]) < 8:
            print("You are using Python 3." + str(sys.version_info[1]))
            print("Commstatx requires Python 3.8 or newer")
            # raise Exception("Wrong Python cannot continue")
            sys.exit()
        else:
            print("Appropriate version of Python found : Python 3." + str(
                sys.version_info[1]) + ", continuing installation")

    except:
        print("Exception while testing Python version, cannot continue installation")
        sys.exit()
    if "Windows" in osver:
        print("Installing for Windows 10 or 11")
        wininstall()
    elif "pi" or "Linux" in osver:
        print("Installing for Linux Mint 20-21 Mate or Pi4 Bullseye 64bit")
        lininstall()
    else:
        print("system not recognized")


def lininstall():
    # firstmodule = "pyqt5"
    # secondmodule = "PyQtWebEngine"
    thirdmodule = "feedparser"
    forthmodule = "file-read-backwards"
    fifthmodule = "folium"
    sixthmodule = "pandas"
    seventhmodule = "maidenhead"
    # install(firstmodule)
    # install(secondmodule)
    install(thirdmodule)
    install(forthmodule)
    install(fifthmodule)
    install(sixthmodule)
    install(seventhmodule)
    runsettings()


def wininstall():
    firstmodule = "pyqt5"
    secondmodule = "PyQtWebEngine"
    thirdmodule = "feedparser"
    forthmodule = "file-read-backwards"
    fifthmodule = "folium"
    sixthmodule = "pandas"
    seventhmodule = "maidenhead"
    install(firstmodule)
    install(secondmodule)
    install(thirdmodule)
    install(forthmodule)
    install(fifthmodule)
    install(sixthmodule)
    install(seventhmodule)
    runsettings()


oscheck()

# test_python()


# os.chdir(os.path.dirname(__file__))
# print(os.getcwd())

# runsettings()
