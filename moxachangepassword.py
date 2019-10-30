# coding=UTF-8


import telnetlib
import time
import sys
import os
import getpass
from datetime import datetime

# 檔案與時間變數設定
dayFomate = datetime.now().strftime('%Y%m%d')
logtimeFomate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
beErrLog = dayFomate+"-"+"beErrLog.log"
beipErrLog = dayFomate+"-"+"iplist_log.log"
doOkLog = dayFomate+"-"+"deOkLog.log"

#等候回應時間
stime = 2

# 睡眠時間函數
def gosleep(x):
    time.sleep(x)

# 寫記錄檔函數
def writeLog(filename,ip,message):
    with open(filename, 'a+') as f:
        f.write('%s : %s : %s\n' % (logtimeFomate,ip,message))

# 寫ip記錄檔函數
def onlyipLog(filename,ip):
    with open(filename, 'a+') as f:
        f.write('%s\n' % (ip))

# 定義密碼
oldpassword = getpass.getpass("請輸入舊密碼: ")
newpassword = getpass.getpass("請輸入新密碼: ")

#  HOST = "192.168.127.254"

# 主要處理更換密碼函數
def changepasww(HOST):
    global oldpassword,newpassword
    try:
        passcheck = 0
        tn = telnetlib.Telnet(HOST,23,5)
        gosleep(stime)

        v = tn.read_very_eager().decode('ascii')
        # print(v)
        if (v.find("Please")) != -1:
            tn.read_until(b"Please keyin your password:",3)
            tn.write(oldpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(b"9\r\n")
            gosleep(stime)
            tn.write(oldpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(newpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(newpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(b"y\r\n")
            gosleep(stime)
            tn.write(b"s\r\n")
            gosleep(stime)
            passcheck = 1
            tn.write(b"y\r\n")
            # print(tn.read_very_eager())
            print(tn.read_all().decode('ascii'))
        
        else:
            oldpassword = ""
            gosleep(stime)
            tn.write(b"9\r\n")
            gosleep(stime)
            tn.write(oldpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(newpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(newpassword.encode('ascii') + b"\r\n")
            gosleep(stime)
            tn.write(b"y\r\n")
            gosleep(stime)
            tn.write(b"s\r\n")
            gosleep(stime)
            passcheck = 1
            tn.write(b"y\r\n")
            # print(tn.read_very_eager())
            print(tn.read_all().decode('ascii'))

    except Exception as e:
        
        if passcheck == 0:
            print('%s : %s\n' % (HOST,e))
            writeLog(beErrLog,HOST,e)
            onlyipLog(beipErrLog,HOST)

        else:
            print('%s : %s\n' % (HOST,"密碼修改成功"))
            writeLog(doOkLog,HOST,"密碼修改成功")
        pass

#程式開始----start
try:
    f = open("iplist.txt", "r")
    for ip in f.readlines():
        ip = ip.strip()
        changepasww(ip)
    f.close()
except Exception as e:
    if e:
        print(e)
        writeLog(beErrLog,"SYSTEM",e)
        sys.exit(1)
