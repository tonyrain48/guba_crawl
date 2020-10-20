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


def loadCodeList():
	return open('allCode.txt').read().split('\n')

codeList = loadCodeList()
for eachCode in codeList:
	codeNum = eachCode[:-3]
	print codeNum
	lines = open('%s.csv' % codeNum).read().split('\n') 
	resultFile = open('new_%s.csv' % codeNum, 'w')  
	for eachLine in lines:
		if eachLine == '\n' or eachLine =='':
			continue
		allCommaUnit = eachLine.split(',')
		title = '|'.join(allCommaUnit[2:-4])
		title = title.decode('GBK')
		title = title.replace('，', '|')
		resultFile.write('%s,%s,%s,%s,%s,%s,%s\n' % (allCommaUnit[0],allCommaUnit[1], title.encode('GBK'), allCommaUnit[-4], allCommaUnit[-3],allCommaUnit[-2],allCommaUnit[-1]))

	resultFile.close()







