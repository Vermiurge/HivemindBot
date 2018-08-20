#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader

def tweetBot(authfile=None):
	j = jsonloader.loadJson(authfile)
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
	#WARNING: Make sure you change the file name here to the correct one
	#There's your goddamn commandline argument
	#look it even has a default
	if sys.argv[1]:
		tweetBot(sys.argv[1])
	else:
		tweetBot("data/auth.json")