#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader, botClass, logging

def tweetBot(tweetDelay, jsonContents, loggingObj, autolog = True, censorBypass = True):
	tb = botClass.TweetBot(jsonContents, loggingObj)
	tb.startBot(loggingObj)

def censored(pfile, pstring):
	with open(pfile, 'r') as f:
		for word in f:
			if word.replace("\n", "") in pstring:
				return True
	f.close()
	return False

def tweet(ptweetAPI, pmessage, ptweetDelay):
	ptweetAPI.update_status(pmessage)
	print("Tweeted: " + pmessage)
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

	tweetBot(1800, j, record, True)	

	#Should I function this out? ¯\_(ツ)_/¯
	with open(j["files"]["logging"], "w+", encoding='utf-8') as f:
		f.write(str(record.getLog()[0]) + "\n")
		for item in record.getLog()[1:]:
			f.write("\t" + str(item) + '\n')
		f.write("Logging Closed")
		f.close()

	exit()
