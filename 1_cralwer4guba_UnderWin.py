#coding=utf-8
import json
import sys
import urllib.request
import re
import codecs
import json
import os
import socket
import threading 
import time
#from bs4 import BeautifulSoup
socket.setdefaulttimeout(50)
# reload(sys)
# sys.setdefaultencoding('utf8')

tryTimes = 3
writeLock = threading.Lock()
writeDoneWorkLock = threading.Lock()



#type 0,justopen, 1,gb2312, 2,gbk, 3,GBK, 4,utf-8
def getPageWithSpecTimes(decodeType, url):
    global tryTimes
    alreadyTriedTimes = 0
    html = None
    while alreadyTriedTimes < tryTimes:
        try:
            if decodeType == 0:
                html = urllib.request.urlopen(url).read()
            elif decodeType == 1:
                html = urllib.request.urlopen(url).read().decode('gb2312', 'ignore').encode('utf8')
            elif decodeType == 2:
                html = urllib.request.urlopen(url).read().decode('gbk', 'ignore').encode('utf8')
            elif decodeType == 3:
                html = urllib.request.urlopen(url).read().decode('GBK', 'ignore').encode('utf8')
            else:
                html = urllib.request.urlopen(url).read()
            break
        except Exception as ep:
            if alreadyTriedTimes < tryTimes - 1:
                alreadyTriedTimes += 1
                pass
            else:
                return None
    return html

def writeMapping(url, path):
    writeLock.acquire()

    filehandler = open('Mapping_baidu.csv','a')
    filehandler.write(url+','+path+'\n')
    filehandler.close()

    writeLock.release()


def writeProcess(processPath, content):
    filehandler = open(processPath, 'w')
    filehandler.write(content)
    filehandler.close()

def writeToLog(content):
    filehandler = open('log.txt', 'a')
    filehandler.write(content)
    filehandler.close()

def loadCodeList():
    #return open('allCode.txt').read().split('\n')
    return open('allCode.txt').read().split('\n')


class DownloadOnePage(threading.Thread):
    #三个参数分别为start，eachlen，totallen
    def __init__(self, code, pageUrl):
        threading.Thread.__init__(self)
        self.pageUrl = pageUrl
        self.code = code

    def run(self):
        #code,id,title,noclick,noreply,potime,udtime
        pageUrl = self.pageUrl
        code = self.code

        pageContent = getPageWithSpecTimes(0, pageUrl)
        pageContent=pageContent.decode('utf-8')
        if pageContent == None:
            writeToLog('cannot open page,%s,%s\n' % code, pageUrl)
            return
        eachDivPatten = re.compile(r'<div class="articleh">(.+?)</div>', re.S)
        allDivList = eachDivPatten.findall(pageContent)
        print(len(allDivList))
        #return

        #pagesoup = BeautifulSoup(pageContent, from_encoding='utf8')

        #allTieziList = pagesoup.find_all('div', attrs={'class':"articleh"})

        for eachTieziLink in allDivList:
            tieziLinkString = str(eachTieziLink)
            print(tieziLinkString)
            #print eachTieziLink
            #return



            urlPattern = re.compile(r'a href="([^"]+?)" title')
            titlePattern = re.compile(r'title="(.+?)" >', re.S)
            readNumPattern = re.compile(r'<span class="l1">(\d+?)</span>')
            commentNumPattern = re.compile(r'<span class="l2">(\d+?)</span>')
            distributeTimePattern = re.compile(r'<span class="l6">(.+?)</span>')
            updateTimePattern = re.compile(r'<span class="l5">(.+?)</span>')


            #readNum = eachTieziLink.find_all('span', attrs={'class':'l1'})[0].get_text()
            #commentNum = eachTieziLink.find_all('span', attrs={'class':'l2'})[0].get_text()
            #distributeTime = eachTieziLink.find_all('span', attrs={'class':'l6'})[0].get_text()
            #updateTime = eachTieziLink.find_all('span', attrs={'class':'l5'})[0].get_text()
            #print readNum, commentNum, distributeTime, updateTime
            #return

            url = None
            title = None
            tieziId = None
            try:
                url = 'http://guba.eastmoney.com' + urlPattern.findall(tieziLinkString)[0]
                tieziId = url.split(',')[-1].split('.')[0]
                title = titlePattern.findall(tieziLinkString)[0]
                title=re.sub(r'\s', '', title)
                readNum = readNumPattern.findall(tieziLinkString)[0]
                commentNum = commentNumPattern.findall(tieziLinkString)[0]
                distributeTime = distributeTimePattern.findall(tieziLinkString)[0]
                updateTime = updateTimePattern.findall(tieziLinkString)[0]



            except Exception as ep:
                print(code, pageUrl)
                print(ep.message)

                print(tieziLinkString)
                pass
            if url != None and title != None and tieziId != None:
                writeLock.acquire()
                filehandler = open('%s.csv' % code, 'a')
                filehandler.write('%s,%s,%s,%s,%s,%s,%s\n' % (code, tieziId, title.encode('GBK','replace'), readNum, commentNum, distributeTime, updateTime) )
                filehandler.close()
                writeLock.release()






        



#processOnePerson('范冰冰')
#sys.exit()



def writeDoneWork(name):
    writeDoneWorkLock.acquire()
    
    filehandler = open('doneWork_downloadPicsUrlTieba.txt', 'a')
    filehandler.write(name)
    filehandler.close()
    
    writeDoneWorkLock.release()

def loadDoneWork():
    try: 
        #doneWorkListPath = os.path.join(doneWorkPath, 'doneWork_downloadPicsUrlTieba.txt')
        return open('doneWork_downloadPicsUrlTieba.txt').read().split('\n')
    except Exception as ep:
        return []


def getListFromFile(fileName):
    namelist = []
    for line in open(fileName):
        for line2 in line.split('\r'):
            line2 = re.sub(r'\n', '', line2)
            if line2 != '':
                namelist.append(line2)

    return namelist


def formCode(stockCode, type):
    # type == 1, 深市A股股票代码
    if type == 1:
        if stockCode < 10:
            return '00000'+str(stockCode)
        elif stockCode < 100:
            return '0000' + str(stockCode)
        elif stockCode < 1000:
            return '000' + str(stockCode)
    # type == 2, 沪市A股股票代码以600开头
    elif type == 2:
        if stockCode < 10:
            return '60000'+str(stockCode)
        elif stockCode < 100:
            return '6000' + str(stockCode)
        elif stockCode < 1000:
            return '600' + str(stockCode)
    # 沪市A股股票代码以601开头
    else:
        if stockCode < 10:
            return '60100'+str(stockCode)
        elif stockCode < 100:
            return '6010' + str(stockCode)
        elif stockCode < 1000:
            return '601' + str(stockCode)



# allAStockCodeFile = open('allAStockCodeFile.txt', 'a')
# allFileInfo = open('allinfo.txt').read()
# for i in range(0, 1000):
#     szCode = formCode(i, 1)
#     if szCode in allFileInfo:
#         allAStockCodeFile.write(szCode+'\n')

# for i in range(0, 1000):
#     shCode1 = formCode(i, 2)
#     if shCode1 in allFileInfo:
#         allAStockCodeFile.write(shCode1+'\n')

# for i in range(0, 1000):
#     shCode2 = formCode(i, 3)
#     if shCode2 in allFileInfo:
#         allAStockCodeFile.write(shCode2+'\n')
# allAStockCodeFile.close()

def getPageNum(code, url):
    pageContent = getPageWithSpecTimes(0, url)
    pageContent=pageContent.decode('utf-8')
    if pageContent == None:
        writeToLog('cannot get page Num for,%s,%s\n' % (code, url))
        return None
    print(pageContent)
    tieziNumPattern = re.compile(r'data-pager="list,([^"]+?)">')
    tieziNumString = tieziNumPattern.findall(pageContent)[0]
    tieziNum = int(tieziNumString.split('|')[1])
    eachPageTieziNum = int(tieziNumString.split('|')[2])
    pageNum = int(tieziNum / eachPageTieziNum) + 1
    return pageNum

#DownloadOnePage('000001', 'http://guba.eastmoney.com/list,000001_920.html').start()
#sys.exit()

threadNum = 100
threadNumPool = {}

codeList = loadCodeList()
for eachCode in codeList:
    print('processing code %s' % eachCode)
    codeNum = eachCode[:-3]
    getPageUrl = 'http://guba.eastmoney.com/list,%s.html' % codeNum
    pageNum = getPageNum(codeNum, getPageUrl)
    for i in range(pageNum):
        #print 'processing %s' % (i+1)
        pageUrl = 'http://guba.eastmoney.com/list,%s_%s.html' % (codeNum, i+1)
        findThread = False
        while findThread == False:
            for j in range(threadNum):
                if j not in threadNumPool:
                    threadNumPool[j] = DownloadOnePage(codeNum, pageUrl)
                    threadNumPool[j].start()
                    findThread = True
                    break
                else:
                    if not threadNumPool[j].isAlive():
                        threadNumPool[j] = DownloadOnePage(codeNum, pageUrl)
                        threadNumPool[j].start()
                        findThread = True
                        break
            if findThread == False:
                time.sleep(5)





