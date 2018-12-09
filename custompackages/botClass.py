#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy as t
import time
from custompackages import jsonloader, logging

class TweetBot:
	def __init__(self, jsonData, delay = 60 * 60 / 2, autolog = True, censorBypass = False):
		auth = t.OAuthHandler(jsonData["auth"]["com_key"], jsonData["auth"]["com_secret"])
		auth.set_access_token(jsonData["auth"]["access_key"], jsonData["auth"]["access_secret"])
		self.delay = delay
		self.autolog = autolog
		self.censorBypass = censorBypass
		self.api = t.API(auth)
		self.encoding =  'utf-8'
		self.tweets = jsonloader.loadJson(jsonData["files"]["tweets"])
		with open(jsonData["files"]["censor"]) as myFile:
			self.censor = []
			for word in myFile:
				self.censor.append(word.replace("\n",""))
		myFile.close() 

	def __repr__(self):
		return "TweetBot(%s,%s,%s,%s)" % (self.jsonData.__repr__(), self.delay, self.autolog, self.censorBypass)

	def setEncoding(self, encoding):
		self.encoding = encoding

	def startBot(self, loggingObj):	
		#starts tweeting from the bottom of the json file
		#assuming bottom is earliest posts going to most recent at top
		for message in reversed(self.tweets['data']):
			try:
				#tweets everything if censorBypass isn't false
				message = message['message']
				length = len(message)
				if self.censorBypass:
					#280 character limit is pretty hardlocked for now, that's why I'm comfortable leaving this as a magic number
					if length <= 280:
						#tweet(api, message, tweetDelay)
						print(message, "\n######")
						pass
					loggingObj.add(message, len(message), self.autolog, False)
					continue
				#tweets only those not caught by the censor
				censored = self.censorTweet(message.lower())
				if not censored:
					if length <= 280:
						#tweet(api, message, tweetDelay)
						print(message, "\n######")
						pass
				loggingObj.add(message, len(message), self.autolog, censored)
			except KeyError as e:
				loggingObj.add("KeyError: entry missing " + str(e))
				continue
	

	def tweet(self, pmessage, ptweetDelay):
		self.api.update_status(pmessage)
		print("Tweeted: " + pmessage)
		time.sleep(ptweetDelay)

	def censorTweet(self, pmessage):
		for word in self.censor:
			if word.replace("\n", "") in pmessage:
				return True
		return False