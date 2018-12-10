#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tweepy, time, sys
from custompackages import jsonloader, botClass, logging

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

	botClass.TweetBot(j, 60*60/2, True).startBot(record)

	record.writeToFile(j["files"]["logging"])

	sys.exit()
