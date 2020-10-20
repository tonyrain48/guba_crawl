#coding=utf-8
import json
import sys
import urllib2, urllib
import re
import codecs
import json
import os
import socket
import threading 
import time
import csv
socket.setdefaulttimeout(50)
reload(sys)
sys.setdefaultencoding('utf8')

tryTimes = 3
writeLock = threading.Lock()
writeDoneWorkLock = threading.Lock()

class DownloadPostInfo(threading.Thread):
    #三个参数分别为start，eachlen，totallen
    def __init__(self, lines, resultFile):
        threading.Thread.__init__(self)
        self.resultFile = resultFile
        self.lines = lines

    def run(self):
        #code,id,title,noclick,noreply,potime,udtime
        resultFile = self.resultFile
        lines = self.lines
        for eachLine in lines:
            if eachLine == '\n' or eachLine =='':
                continue
            allCommaUnit = eachLine.split(',')
#            print allCommaUnit[0]
#            print allCommaUnit[1]
            getPageUrl = 'http://guba.eastmoney.com/news,%s,%s.html' % (allCommaUnit[0],allCommaUnit[1])
#            print getPageUrl
            postinfo = getPostInfo(codeNum, getPageUrl)
            print(postinfo)
            resultFile.write('%s,%s,%s\n' % (allCommaUnit[0],allCommaUnit[1],postinfo))
        resultFile.close()
 

def getPageWithSpecTimes(decodeType, url):
    global tryTimes
    alreadyTriedTimes = 0
    html = None
    while alreadyTriedTimes < tryTimes:
        try:
            if decodeType == 0:
                html = urllib.urlopen(url).read()                
            elif decodeType == 1:
                html = urllib.urlopen(url).read().decode('gb2312', 'ignore').encode('utf8')
            elif decodeType == 2:
                html = urllib.urlopen(url).read().decode('gbk', 'ignore').encode('utf8')
            elif decodeType == 3:
                html = urllib.urlopen(url).read().decode('GBK', 'ignore').encode('utf8')
            else:
                html = urllib.urlopen(url).read()
            break
        except Exception as ep:
            if alreadyTriedTimes < tryTimes - 1:
                alreadyTriedTimes += 1
                pass
            else:
                return None
    return html

def loadCodeList():
    return open('allCode.txt').read().split('\n')

def getPostInfo(code, url):
    pageContent = getPageWithSpecTimes(0, url)
    if pageContent == None:
        writeToLog('cannot get page tiezi for,%s,%s\n' % (code, url))
        return None
    tieziNumPattern = re.compile(r'发表于([^"]+?)</div>')
    tieziNumString = tieziNumPattern.findall(pageContent)[0]
    tieziNum = tieziNumString.split(' ')[1]
    return tieziNum


threadNum = 4
threadNumPool = {}

codeList = loadCodeList()
for eachCode in codeList:
    codeNum = eachCode[:-3]
    print(codeNum)
    lines = open('new_%s.csv' % codeNum).read().split('\n') 
    resultFile = open('newt_%s.csv' % codeNum, 'w')  

    findThread = False
    while findThread == False:
        for j in range(threadNum):
            if not threadNumPool.has_key(j):
                threadNumPool[j] = DownloadPostInfo(lines, resultFile)
                threadNumPool[j].start()
                findThread = True
                break
            else:
                if not threadNumPool[j].isAlive():
                    threadNumPool[j] = DownloadPostInfo(lines, resultFile)
                    threadNumPool[j].start()
                    findThread = True
                    break
        if findThread == False: 
            time.sleep(5)






