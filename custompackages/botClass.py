#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy as t
import time
from custompackages import jsonloader, logging

class TweetBot:
	'TweetBot(jsonData, delay, autolog, censorBypass)'
	def __init__(self, jsonData, delay = 60 * 60 / 2, autolog = True, censorBypass = False):
		auth = t.OAuthHandler(jsonData["auth"]["com_key"], jsonData["auth"]["com_secret"])
		auth.set_access_token(jsonData["auth"]["access_key"], jsonData["auth"]["access_secret"])
		self.jsonData = jsonData
		self.delay = delay
		self.autolog = autolog
		self.censorBypass = censorBypass
		self.api = t.API(auth)
		self.encoding =  'utf-8'
		self.tweets = jsonloader.loadJson(self.jsonData["files"]["tweets"], self.encoding)
		with open(self.jsonData["files"]["censor"]) as myFile:
			self.censor = []
			for word in myFile:
				self.censor.append(word.replace("\n",""))
		myFile.close() 

	def __repr__(self):
		return "TweetBot(%s,%s,%s,%s)" % (self.jsonData.__class__.__name__, self.delay, self.autolog, self.censorBypass)

	def setEncoding(self, encoding):
		self.encoding = encoding
		self.tweets = jsonloader.loadJson(self.jsonData["files"]["tweets"], self.encoding)

	def startBot(self, loggingObj):	
		#starts tweeting from the bottom of the json file
		#assuming bottom is earliest posts going to most recent at top
		censored = False
		for message in reversed(self.tweets['data']):
			try:
				message = message['message']
				length = len(message)
				
				#tweets everything if censorBypass isn't false
				if not self.censorBypass:
					censored = self.censorTweet(message.lower())
				
				if length <= 280 and not censored:
					#tweet(message)
					print(message, "\n###############")
				loggingObj.add(message, length, self.autolog, censored)
			except KeyError as e:
				loggingObj.add("KeyError: entry missing " + str(e))
				continue
	
	def tweet(self, pmessage):
		self.api.update_status(pmessage)
		print("Tweeted: " + pmessage)
		time.sleep(self.delay)

	def censorTweet(self, pmessage):
		for word in self.censor:
			if word.replace("\n", "") in pmessage:
				return True
		return False