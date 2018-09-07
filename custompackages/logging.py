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
		#To check for the autologging flag
		if pTime ==  True:
			self.logtime = time.strftime(self.timeFormat, time.localtime())
		else:
			self.logtime = pTime
	
	def __str__(self):
		prefix = ""
		if self.logtime != None:
			prefix = "[" + str(self.logtime) + "]: " 
		return str(prefix + super().__str__())

	def __repr__(self):
		return "logEntryTimestamped(\"%s\", %s)" % (self.message, self.logtime)
	
class logEntryPost(logEntryTimestamped):
	logEntryTimestamped.timeFormat = "%H:%M:%S %a %d-%m-%y"
	def __init__(self, pMessage, pCharacters, pTime = None, pCensor = False):
		super().__init__(pMessage, pTime)
		self.censored = pCensor
		self.characters = pCharacters
	def __str__(self):
		return "%s | Censored = %s | %i characters" % (super().__str__(), self.censored, self.characters)
		#return super().__str__() + " | Censored = " + str(self.censored)
	def __repr__(self):
		return "logEntryPost(\"%s\", %s, %s)" % (self.message, self.logtime, self.censored)
	
class log:
	def __init__(self):
		self.logstack = []
		self.logstack.append(logBaseEntry("-------Logging Started-------"))

	def getLog(self):
		return self.logstack

	def add(self, pMessage, pCharacters =  None, pTime = None, pCensor = None):
		if pCensor != None:
			self.logstack.append(logEntryPost(pMessage, pCharacters,pTime, pCensor))
			return
		elif pTime != None:
			self.logstack.append(logEntryTimestamped(pMessage, pTime))
			return
		else:
			self.logstack.append(logBaseEntry(pMessage))
			return
