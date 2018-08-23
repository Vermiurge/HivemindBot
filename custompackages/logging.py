#!/usr/bin/python3

import time

class logEntry:
	time  = ""
	message = ""
	timeFormat = "%H:%M:%S"
	def __init__(self, pMessage, pTime = None):
		if pTime:
			self.time = pTime
		else:
			self.time = time.strftime(self.timeFormat, time.localtime())
		self.message = pMessage
	def __repr__(self):
		return str(self.time) + " : " + str(self.message)

class logEntryPost(logEntry):
	censored = None
	logEntry.timeFormat = "%H:%M:%S %a %d-%m-%y"
	def __init__(self, pMessage, pTime = None, pCensor = False):
		logEntry.__init__(pMessage, pTime)
		self.censored = pCensor
	def __repr__(self):
		return logEntry.__repr__() + " | Censored = " + str(pCensor)




class log:
	logstack = []
	def __init__(self):
		self.logstack.append(logEntry("Start", 1))

	def getLog(self):
		return self.logstack

	def add(self, pMessage, pTime = None, pCensor = None):
		if pCensor != None:
			self.logstack.append(logEntryPost(pMessage, pTime, pCensor))
		else:
			self.logstack.append(logEntry(pMessage, pTime))
