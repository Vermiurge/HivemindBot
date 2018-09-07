#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader, logging

def tweetBot(tweetDelay, jsonContents, autolog = True):
	try:
		d = jsonContents["auth"]
		data = jsonContents["files"]
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
				#TODO: Respect the 240 character limit
				#tweets everything if censorBypass isn't false
				message = message['message']
				length = len(message)
				if censorBypass:
					#280 character limit is pretty hardlocked for now, that's why I'm comfortable leaving this as a magic number
					if length > 280:
						#tweet(api, message, tweetDelay)
						#print(message, "\n######")
						pass
					record.add(message, len(message),autolog, false)
					continue
				#tweets only those not caught by the censor
				censorTweet = censored(censor, message.lower())
				if not censorTweet:
					if length > 280:
						#tweet(api, message, tweetDelay)
						#print(message, "\n######")
						pass
				record.add(message, len(message), autolog, censorTweet)
			except KeyError as e:
				record.add("KeyError: entry missing "+ str(e))
				continue
	f.close()

	for item in record.getLog():
		print(str(item))


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
		j = jsonloader.loadHjson(sys.argv[1])
		record.add(str(sys.argv[1]) + " opened")
	except IndexError as e:
		j = jsonloader.loadHjson(defaultPath)
		record.add(defaultPath + " opened")

	tweetBot(1800, j, True)	

	#Should I function this out? ¯\_(ツ)_/¯
	with open(j["files"]["logging"], "w+", encoding='utf-8') as f:
		f.write(str(record.getLog()[0]) + "\n")
		for item in record.getLog()[1:]:
			f.write("\t" + str(item) + '\n')
		f.write("Logging Closed")
		f.close()

	exit()
