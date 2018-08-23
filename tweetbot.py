#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader, logging

def tweetBot(tweetDelay, authfile=None):
	j = jsonloader.loadHjson(authfile)
	
	
	print(record.getLog())

	try:
		d = j["auth"]
		data = j["files"]
	except:
		record.log("Data not found")
	
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

	#I really suggest not changing the encoding especially if emojis are to be expected from the source
	with open(data["tweets"], 'r', encoding='utf-8') as f:
		#starts tweeting from the bottom of the json file
		#assuming bottom is earliest posts going to most recent at top
		for message in reversed(tweets['data']):
			try:
				#These prints are more for debug than anything
				if censorBypass:
					#tweet(api, message['message'], tweetDelay)
					#print(message['message'], "\n######")
					record.add(message['message'])
					continue
				if(not censored(censor, message['message'].lower())):
					#tweet(api, message['message'], tweetDelay)
					#print(message['message'], "\n######")
					record.add(message['message'])
					pass
			except BaseException as e:
				record.add(e)
				continue
	f.close()

	#TODO: implement a more complete logging flow and write results to file
	for item in record.getLog():
		print(item)

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
		tweetBot(1800, sys.argv[1])
		record.add(sys.argv[1], " opened")
	except:
		tweetBot(1800, defaultPath)
		record.add(defaultPath, " opened")

	exit()
