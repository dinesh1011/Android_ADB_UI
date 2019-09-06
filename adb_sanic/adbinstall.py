
from __future__ import print_function
import subprocess
import os
import sys
import time
import re

def get_devices():
    devices = {}
    getdevices = subprocess.Popen("adb devices -l | tail -n +2 | awk '{for(i=1;i<=NF;i++){if(match($i,/model:/)){print $1"'","'"$i}} }' ", stdout=subprocess.PIPE, shell=True)
    for device in getdevices.stdout:
        if(device.decode("UTF-8").strip(" \t\r\n") != ""):
            devicesplit = device.decode("UTF-8").strip(" \t\r\n").split(",")
            deviceid = devicesplit[0]
            devicemodel = devicesplit[1]
            devices[deviceid] = devicemodel
    getdevices.kill()
    return devices

def get_installed_packages(deviceid):
    packages = []
    get_packages = subprocess.Popen("adb -s %s shell pm list packages -3 |cut -d'"':'"' -f2" %deviceid, stdout=subprocess.PIPE, shell=True)
    for package in get_packages.stdout:
        if(package.decode("UTF-8").strip(" \t\r\n") != ""):
            packages.append(package.decode("UTF-8").strip(" \t\r\n"))
    get_packages.kill()
    print(packages)
    return packages


def uninstall_package(deviceid, packages):
    outputStatus = {}
    for app in packages:
        uninstal_command = "adb -s %s uninstall %s"  %(deviceid, app)
        print(uninstal_command)
        uninstall = subprocess.run(uninstal_command, stdout=subprocess.PIPE, shell=True)
        print(uninstall.stdout)
        statusString = uninstall.stdout
        outputStatus[app] = statusString.decode("UTF-8").strip("\r\n\t")
    return outputStatus


def install_packages(idevice, iapps):
    apps = iapps.split("|")
    outputStatus = {}
    for iapp in apps:
        app = verify_app_path(iapp)
        if(app == False):
            outputStatus[iapp] =  "Invalid apk Url or Path"
            continue
        iapp = iapp.replace(" ","\ ").replace("(", "\(").replace(")", "\)")
        print("test ---- " + iapp)
        instal_command = "adb -s %s install %s"  %(idevice, iapp)
        print(instal_command)
        install = subprocess.run(instal_command, stdout=subprocess.PIPE, shell=True)
        #print(install.stdout)
        statusString = install.stdout
        statusStringList = statusString.decode("UTF-8").split("\n")
        outputStatus[iapp] = statusStringList[len(statusStringList)-2]
    return outputStatus

def verify_app_path(appUrl):
    matchFound = re.match(".*\.apk", appUrl)
    if(matchFound):
        return True
    return False

def install_package(daxDevice, apptype="none"):
    statusString = ""
    outputStatus = {}

    BUILD_DAX_PATH = ""
    if(apptype == "DAX"):
        BUILD_DAX_PATH = "/Users/dinesh.duraisamy/Documents/DAX/test_builds/"
    elif(apptype == "PAX"):
        BUILD_DAX_PATH = "/Users/dinesh.duraisamy/Documents/PAX/test_builds/"
    else:
        return " Please provide apptype as PAX or DAX"

    command_string = "ls -litr " + BUILD_DAX_PATH + "| tail -n 1 | awk '{print $10}'"
    latest_build_file = subprocess.Popen(command_string, stdout=subprocess.PIPE, shell=True)
    latest_file_path = ""
    for lin in latest_build_file.stdout:
        print(lin)
        latest_file_path = BUILD_DAX_PATH + lin.decode("UTF-8").strip("\r\n\t")
    print(latest_file_path)
    instal_command = "adb -s %s install %s"  %(daxDevice, latest_file_path)
    print(instal_command)
    install = subprocess.run(instal_command, stdout=subprocess.PIPE, shell=True)
    statusString = install.stdout
    outputStatus[apptype] = statusString.decode("UTF-8").strip("\r\n\t")
    return outputStatus
