# -*- coding:utf-8 -*-
# !/usr/bin/env python
################################################################################
#
# Copyright (c) 2018 , Inc. All Rights Reserved
#
################################################################################
"""
This is a simple job be use for self by auto checkin 23333
author Richar(chigco@gmail.com)
"""
# modify history list

# thinking init 
# 2018-07-19 21:48:02

# 修复休眠时间负数导致程序睡死
# 增加时间转换动态随机日期一开始便创建好
# 增加日志输出函数调用
# 2018-8-3 10:37:12


import io

import urllib2
import cookielib
import os
import sqlite3
import win32crypt

import chardet
import urllib
#from win32.win32crypt import CryptUnprotectData
from bs4 import BeautifulSoup 
import ConfigParser
import schedule
import time
import random
import threading
import datetime

import sys   


host = ''           # 主机地址带http://
path = ''           # 一级目录带 /
signUrl = ''        # Sign获取地址
checkInUrl = ''     # 签到日志地址
timePieces = 0      # 时间间隙
times = ''          # 时间HH:mm
content = ''        # 签到内容
weeks = 0           # 是否每周开启

def getCookieFromChrome(host):
    cookiepath = os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s' limit 1" % host
    #sql="select host_key,name,encrypted_value from cookies"
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()        
        #for host_key,name,encrypted_value in cu.execute(sql).fetchall():
           #print(win32crypt.CryptUnprotectData(encrypted_value)[1].decode())
        cookies = {name:win32crypt.CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        #print(cookies)
        log("[4/6] GET COOKIE...")
        # time_stamp = datetime.datetime.now()
        # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [4/6] GET COOKIE..."
        return cookies

def getSettingFromFile(file='setting.ini'):
    conf = ConfigParser.ConfigParser()
    conf.read(file)       # 文件路径
    host = conf.get("common", "application.host") # 获取指定section 的option值
    path = conf.get("common", "application.path") # 获取指定section 的option值
    signUrl = conf.get("common", "application.sign.url") # 获取指定section 的option值
    checkInUrl = conf.get("common", "application.checkin.url") # 获取指定section 的option值
    weeks = conf.get("common", "application.every.weeks") # 获取指定section 的option值
    timePieces = conf.get("checkin", "application.time.pieces") # 获取指定section 的option值
    times = conf.get("checkin", "application.check.time") # 获取指定section 的option值
    content = conf.get("checkin", "application.check.content") # 获取指定section 的option值
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [1/6] READ SETTING OK..."
    log("[1/6] READ SETTING OK...")
    return host,path,signUrl,checkInUrl,timePieces,times,content,weeks

# def setTimer(time,interval,host,path,signUrl,checkInUrl,content):
def setTimer():
    flg = ''
    if int(weeks) == 1:
        # schedule.every().week.at(times).do(task)
        taskTime = intervalTaskTime()
        log("[DEBUG] monday:" + taskTime)
        schedule.every().monday.at(taskTime).do(task)
        taskTime = intervalTaskTime()
        log("[DEBUG] tuesday:" + taskTime)
        # print "tuesday:" + taskTime
        schedule.every().tuesday.at(taskTime).do(task)
        taskTime = intervalTaskTime()
        log("[DEBUG] wednesday:" + taskTime)
        # print "wednesday:" + taskTime
        schedule.every().wednesday.at(taskTime).do(task)
        taskTime = intervalTaskTime()
        log("[DEBUG] thursday:" + taskTime)
        # print "thursday:" + taskTime
        schedule.every().thursday.at(taskTime).do(task)
        taskTime = intervalTaskTime()
        log("[DEBUG] friday:" + taskTime)
        # print "friday:" + taskTime
        schedule.every().friday.at(taskTime).do(task)
        flg = 'week'
    elif int(weeks) == 0:
        schedule.every().day.at(taskTimeStr).do(task)
        flg = 'day'
    # schedule.every().monday.at(times).do(task)
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [2/6] SET SCHEDULE OK..." + flg + " " + times
    # log("[2/6] SET SCHEDULE OK..." + flg + " " + times)
    # schedule.every(5).seconds.do(task)
    
def intervalTaskTime():
    ranTime = random.randint(-int(timePieces), int(timePieces))
    log("[DEBUG] ranTime:" + str(ranTime))
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [DEBUG] ranTime:" + str(ranTime)
    taskTime = datetime.datetime.strptime(times,'%H:%M')
    # datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
    delta = datetime.timedelta(minutes=ranTime)
    taskTimeStr = (taskTime + delta).strftime('%H:%M')
    log("[DEBUG] taskTime:" + taskTimeStr)
    return taskTimeStr

def log(log):
    time_stamp = datetime.datetime.now()
    print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] " + log

def task():
    # 获取现在时间
    # now_time = datetime.datetime.now()
    # # 获取明天时间
    # next_time = now_time + datetime.timedelta(days=+1)
    # next_year = next_time.date().year
    # next_month = next_time.date().month
    # next_day = next_time.date().day

    # # 获取明天x点时间
    # next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" " + time, "%Y-%m-%d %H:%M:%S")
    # # 获取距离明天3点时间，单位为秒
    # timer_start_time = (next_time - now_time).total_seconds()
    # timer_start_time += random.randint(-int(interval), int(interval))
    # timer_start_time = 3.0
    # print(timer_start_time)
    # #定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    # timer = threading.Timer(2.0, hello,[host,path,signUrl,checkInUrl,content])
    # timer.start()
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [3/6] RUN TASK..."
    log("[3/6] RUN TASK...")
    threading.Thread(target=checkInProcess,args=(host,path,signUrl,checkInUrl,content)).start()

def checkInProcess(host,path,signUrl,checkInUrl,content):
    if not content.strip():
        content = 1
    # ranTime = random.randint(-int(timePieces), int(timePieces))
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [DEBUG] ranTime:" + str(ranTime)
    # time.sleep(ranTime)
    # 获取本地cookie
    cookie = getCookieFromChrome(host.replace('http://',''))
    devId = cookie["DevId"]
    log("[DEBUG] GetCookie:" + str(devId))
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [DEBUG] GetCookie:" + str(devId)
        # write('cookie.txt',txt)
    # 1.打开获取sign
    #User-Agent信息                   
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    head = {
    # 'User-Agnet': user_agent, 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    "Cookie": 'DevId=' + devId,
    'Referer': host + path
    }

    url = host + path + signUrl #'http://172.16.128.125/h5/addplan.form.php' 
    req1 = urllib2.Request(url=url, headers=head)
    req1.add_header('User-agent', user_agent)
    #创建一个MozillaCookieJar对象
    cookie = cookielib.MozillaCookieJar()
     #利用获取到的cookie创建一个opener
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    res = opener.open(req1)  
    html = res.read()
    # 获取网页编码
    char_type = chardet.detect(html)
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [5/6] GET SIGN..."
    log("[5/6] GET SIGN...")
    # 非utf-8码
    if char_type["encoding"].lower() != 'utf-8':
        html = unicode(html, "gbk").encode("utf8")
    # print html
    #用BeautifulSoup解析数据  python3 必须传入参数二'html.parser' 得到一个对象，接下来获取对象的相关属性
    html=BeautifulSoup(html,'html.parser')
    #    print t
    signInput=html.find_all(id='Sign')
    sign=signInput[0].attrs['value']

    # 2.日志
    url = host + path + checkInUrl #'http://172.16.128.125/h5/addplan.php' 
   
    #Headers信息
    head = {
        # 'User-Agnet': user_agent, 
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        "Cookie": 'DevId=' + devId,
        "Origin": host , #"http://172.16.128.125",
        "Host": host.replace('http://',''),  #"172.16.128.125",
        'Referer': host + path + signUrl #'http://172.16.128.125/h5/addplan.form.php'
        }
    # print devId  
    Login_Data = {
        "LogType": 0,
        "Content": content,
        "Sign": sign
    }
    #使用urlencode方法转换标准格式
    logingpostdata = urllib.urlencode(Login_Data).encode('utf-8')
    #创建Request对象 POST
    req1 = urllib2.Request(url=url,data=logingpostdata, headers=head)
    req1.add_header('User-agent', user_agent)
    #创建一个MozillaCookieJar对象
    cookie = cookielib.MozillaCookieJar()
    #利用获取到的cookie创建一个opener
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    res = opener.open(req1)  
    html = res.read()
    # 获取网页编码
    char_type = chardet.detect(html)
    # print char_type
    # 非utf-8码
    if char_type["encoding"].lower() != 'utf-8':
        html = unicode(html, "gbk").encode("utf8")
    # data = StringIO.StringIO(html)
    # gzipper = gzip.GzipFile(fileobj=data)
    # html = gzipper.read()    
    # print html # .decode('gbk') #.decode('utf-8')
    # time_stamp = datetime.datetime.now()
    # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [6/6] CHECK IN OK..."
    log("[6/6] CHECK IN OK...")
    if int(weeks) == 1:
        log("[2/6] READY?NEXT!..." + times)
        # print "[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] [2/6] READY?NEXT!..." + times
    
if __name__ == '__main__':
    host,path,signUrl,checkInUrl,timePieces,times,content,weeks = getSettingFromFile()
    # getSettingFromFile()
    setTimer()
    #cookie = getCookieFromChrome(host.replace('http://',''))
    while True: 
        schedule.run_pending()
        time.sleep(1)
    raw_input()
    # checkInProcess(host,path,signUrl,checkInUrl,content)
     
  