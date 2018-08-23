#!/usr/bin/python3

import time

class logitem():
	time  = ""
	message = ""
	censored = None
	def __init__(self, pMessage, pTime = None, pCensor = false):
		if pTime:
			self.time = pTime
		else:
			self.time = time.strftime("%H:%M:%S %a %d-%m-%y", time.localtime())
		self.message = pMessage
		self.censored = pCensor
	def __repr__(self):
		return str(self.time) + " : " + str(self.message) 


class log():
	logstack = []
	def __init__(self):
		self.logstack.append(logitem("Start", 1))

	def getLog(self):
		return self.logstack

	def add(self, pMessage, pTime = None):
		self.logstack.append(logitem(pMessage, pTime))

