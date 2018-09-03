#!/usr/bin/python3

import time

class logBaseEntry:
	def __init__(self, pMessage):
		self.message = pMessage
	def __str__(self):
		return str(self.message)
	def __repr__(self):
		return "logBaseEntry(\"%s\")" % self.message

class logEntryTimestamped(logBaseEntry):
	timeFormat = "%H:%M:%S"
	def __init__(self, pMessage, pTime = None):
		super().__init__(pMessage)
		self.logtime = time.strftime(self.timeFormat, time.localtime())
	
	def __str__(self):
		prefix = ""
		if self.logtime != None:
			prefix = "[" + str(self.logtime) + "]: " 
		return str(prefix + super().__str__())

	def __repr__(self):
		return "logEntryTimestamped(\"%s\", %s)" % (self.message, self.logtime)
	
class logEntryPost(logEntryTimestamped):
	logEntryTimestamped.timeFormat = "%H:%M:%S %a %d-%m-%y"
	def __init__(self, pMessage, pTime = None, pCensor = False):
		super().__init__(pMessage, pTime)
		self.censored = pCensor
	def __str__(self):
		return super().__str__() + " | Censored = " + str(self.censored)
	def __repr__(self):
		return "logEntryPost(\"%s\", %s, %s)" % (self.message, self.logtime, self.censored)
	
class log:
	def __init__(self):
		self.logstack = []
		self.logstack.append(logBaseEntry("-------Logging Started-------"))

	def getLog(self):
		return self.logstack

	def add(self, pMessage, pTime = None, pCensor = None):
		if pCensor != None:
			self.logstack.append(logEntryPost(pMessage, pTime, pCensor))
			return
		elif pTime != None:
			self.logstack.append(logEntryTimestamped(pMessage, pTime))
			return
		else:
			self.logstack.append(logBaseEntry(pMessage))
			return
