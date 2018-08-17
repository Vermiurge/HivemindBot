#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader

def tweetBot():
	#WARNING: Make sure you change the file name here to the correct one
	#Should I make this a commandline argument? 
	#Yes
	#Am I going to do it?
	#Look man I just work here
	j = jsonloader.loadJson("data/auth.json")
	d = j["auth"]
	data = j["files"]
	tweets = jsonloader.loadJson(data["tweets"])
	censor = data["censor"]

	COM_KEY = d["com_key"]
	COM_SECRET = d["com_secret"]
	ACCESS_KEY = d["access_key"]
	ACCESS_SECRET = d["access_secret"]

	auth = tweepy.OAuthHandler(COM_KEY, COM_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	print("OAuthed")

	with open(data["tweets"], 'r', encoding='utf-8') as f:
		for message in reversed(tweets['data']):
			try:
				if(not censored(censor, message['message'].lower())):
					api.update_status(message['message'])
					print("Tweeted")
					#NOTE: Change time.sleep() to your liking for how often it should tweet
					time.sleep(1800)
			except:
				continue

	f.close()

def censored(file, string):
	with open(file, 'r') as f:
		for word in f:
			if word.replace("\n", "") in string:
				return True
	f.close()
	return False

if __name__ == '__main__':
	tweetBot()