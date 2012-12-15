# -*- coding: utf-8 -*-
import re, os, sys, cookielib, random
import urllib, urllib2, re, sys, math
import elementtree.ElementTree as ET
import xbmcaddon

import pLog

log = pLog.pLog()

scriptID = sys.modules[ "__main__" ].scriptID
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

HOST_TABLE = { 100: 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0',
	       101: 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11',
	       102: 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.11',
	       103: 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
	       104: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20121213 Firefox/19.0',
	       105: 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/20100101 Firefox/17.0',
	       106: 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11',
	       107: 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       108: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17',
	       109: 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	       110: 'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01',
	       111: 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
	       112: 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
	       113: 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
	    }

HOST = 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0'
HISTORYFILE = ptv.getAddonInfo('path') + os.path.sep + "searchhistory.xml"

cj = cookielib.LWPCookieJar()

CHARS = [
    [ ' ', '_' ],
    [ ',', '-' ],
    [ '!', '_' ],
    [ '?', '_' ],
    [ ':', '_' ],
    [ '/', '-' ],
    [ 'ą', 'a' ],
    [ 'Ą', 'A' ],
    [ 'ę', 'e' ],
    [ 'Ę', 'E' ],
    [ 'ć', 'c' ],
    [ 'Ć', 'C' ],
    [ 'ł', 'l' ],
    [ 'Ł', 'L' ],
    [ 'ń', 'n' ],
    [ 'Ń', 'N' ],
    [ 'ó', 'o' ],
    [ 'Ó', 'O' ],
    [ 'ś', 's' ],
    [ 'Ś', 'S' ],
    [ 'ż', 'z' ],
    [ 'Ż', 'Z' ],
    [ 'ź', 'z' ],
    [ 'Ź', 'Z' ],
]


class common:
    def __init__(self):
        pass
    
    def requestData(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', self.getRandomHost())
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()    
        return data
    
    def getURLFromFileCookieData(self, url, COOKIEFILE):
        cj.load(COOKIEFILE)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        data = response.read()
        response.close()    
        return data

    def postURLFromFileCookieData(self, url, COOKIEFILE, POST = {}):
        cj.load(COOKIEFILE)
        headers = { 'User-Agent' : HOST }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        dataPost = urllib.urlencode(POST)
        req = urllib2.Request(url, dataPost, headers)
        response = opener.open(req)
        data = response.read()
        response.close()
        return data
    
    def saveURLToFileCookieData(self, url, COOKIEFILE, POST = {}):
        headers = { 'User-Agent' : HOST }
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        dataPost = urllib.urlencode(POST)
        req = urllib2.Request(url, dataPost, headers)
        response = opener.open(req)
        data = response.read()
        response.close()
        cj.save(COOKIEFILE)
        return data

    def getURLRequestData(self, url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data 
        
    def makeABCList(self):
        strTab = []
        strTab.append('0 - 9');
        for i in range(65,91):
            strTab.append(str(unichr(i)))	
        return strTab
    
    def getItemByChar(self, char, tab):
        strTab = []
        char = char[0]
        for i in range(len(tab)):
            if ord(char) >= 65:
                if tab[i][0].upper() == char:
                    strTab.append(tab[i])
            else:
                if ord(tab[i][0]) >= 48 and ord(tab[i][0]) <= 57:
                    strTab.append(tab[i])
        return strTab       
    
    def isNumeric(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def checkDir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)
            
    
    def getRandomHost(self):
	host_id = random.choice(HOST_TABLE.keys())
	log.info("host ID: " + str(host_id))
	host = HOST_TABLE[host_id]
	return host
	    
	    
	
class history:
    def __init__(self):
        pass
    
    def readHistoryFile(self):
	file = open(HISTORYFILE, 'r')
	root = ET.parse(file).getroot()
	file.close()
	return root


    def writeHistoryFile(self, root):
	file = open(HISTORYFILE, 'w')
	ET.ElementTree(root).write(file)
	file.close() 


    def loadHistoryFile(self, service):
	if not os.path.isfile(HISTORYFILE):
	    self.makeHistoryFile(service)
	history = self.parseHistoryFile(service)
	return history
    

    def addHistoryItem(self, service, item):
	if not os.path.isfile(HISTORYFILE):
	    self.makeHistoryFile(service)
	strTab = []
	root = self.readHistoryFile()
	#check if item already exists
	exists = False
	for node in root.getiterator(service):
	    for child in node.getchildren():
		if child.text != None:
		    strTab.append(child.text)
		else:
		    strTab.append('')
		if child.text == item:
		    exists = True
	    if not exists:
		print "tab: " + str(strTab)
		i=0
		for node in root.getiterator(service):
		    for child in node.getchildren():
			if i==0: child.text = item
			else: child.text = strTab[i-1]
			i = i + 1
		self.writeHistoryFile(root)
		
		
    def clearHistoryItems(self, service):
	root = self.readHistoryFile()
	for node in root.getiterator(service):
	    for child in node.getchildren():
		child.text = ''
	self.writeHistoryFile(root)


    def parseHistoryFile(self, service):
	strTab = []
	root = self.readHistoryFile()
	serviceList = root.findall(service)
	if len(serviceList) == 0:
	    child = ET.Element(service)
	    root.append(child)   
	    for i in range(5):
		item = ET.Element('search')
		child.append(item)
	    self.writeHistoryFile(root)
	    
	for node in root.getiterator(service):
	    for child in node.getchildren():
		if child.text != None:
		    strTab.append(child.text)
		else:
		    strTab.append('')
	return strTab

    
    def makeHistoryFile(self, service):
	root = ET.Element('history')
	child = ET.Element(service)
	root.append(child)   
	for i in range(5):
	    item = ET.Element('search')
	    child.append(item)
	self.writeHistoryFile(root)


class Chars:
    def __init__(self):
        pass
    
    def setCHARS(self):
        return CHARS
    
    def replaceString(self, array, string):
        out = string
        for i in range(len(array)):
            out = string.replace(array[i][0], array[i][1])
            string = out
        return out    
    
    def replaceChars(self, string):
        out = string
        for i in range(len(CHARS)):
            out = string.replace(CHARS[i][0], CHARS[i][1])
            string = out
        return out        
    