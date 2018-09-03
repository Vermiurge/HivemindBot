#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader, logging

def tweetBot(tweetDelay, authfile=None, autolog = True):
	j = jsonloader.loadHjson(authfile)

	try:
		d = j["auth"]
		data = j["files"]
	except:
		record.add("Data not found")
		return
	
	tweets = jsonloader.loadJson(data["tweets"])
	censor = data["censor"]	
	censorBypass = False
	
	if censor == "":
		censorBypass = True
	
	COM_KEY = d["com_key"]
	COM_SECRET = d["com_secret"]
	ACCESS_KEY = d["access_key"]
	ACCESS_SECRET = d["access_secret"]

	auth = tweepy.OAuthHandler(COM_KEY, COM_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	print("OAuthed")

	#I really suggest not changing the encoding especially if nonASCII characters are to be expected from the source
	with open(data["tweets"], 'r', encoding='utf-8') as f:
		#starts tweeting from the bottom of the json file
		#assuming bottom is earliest posts going to most recent at top
		for message in reversed(tweets['data']):
			try:
				#tweets everything if censorBypass isn't false
				if censorBypass:
					#tweet(api, message['message'], tweetDelay)
					#print(message['message'], "\n######")
					record.add(message['message'], autolog, false)
					continue
				#tweets only those not caught by the censor
				censorTweet = censored(censor, message['message'].lower())
				if not censorTweet:
					#tweet(api, message['message'], tweetDelay)
					#print(message['message'], "\n######")
					pass
				record.add(message['message'], autolog, censorTweet)
			except KeyError as e:
				record.add("KeyError: entry missing "+ str(e))
				continue
	f.close()

	for item in record.getLog():
		print(repr(item))

	#TODO:Find a way to move this out of tweetbot()
	with open(data["logging"], "w+", encoding='utf-8') as f:
		for item in record.getLog():
			f.write(str(item) + '\n')
		f.close()
	

def censored(pfile, pstring):
	with open(pfile, 'r') as f:
		for word in f:
			if word.replace("\n", "") in pstring:
				return True
	f.close()
	return False

def tweet(ptweetAPI, pmessage, ptweetDelay):
	ptweetAPI.update_status(pmessage)
	print("Tweeted")
	time.sleep(ptweetDelay)

if __name__ == '__main__':
	#WARNING: Make sure you change the file name here to the correct one
	#Set the time delay between tweets in seconds
	#I defaulted it to every half hour, 60 X 60 / 2
	record = logging.log()
	defaultPath = "data/auth.hjson"
	try:
		tweetBot(1800, sys.argv[1], True)
		record.add(sys.argv[1], " opened")
	except IndexError:
		tweetBot(1800, defaultPath, True)
		record.add(defaultPath, " opened")

	exit()
