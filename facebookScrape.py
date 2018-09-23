#!/usr/bin/env python3

import requests, json, sys, urllib
from custompackages import jsonloader, logging

def facebookScrape(jsonContents):
	
	try:
		auth = jsonContents['auth']
		files = jsonContents['files']
	except:
		record.add("Data not found")
		return

	#TODO: These do nothing. Remove?
	#APP_ID 		=	auth['app_id']
	#APP_SECRET 	=	auth['app_secret']

	#These pull the Page id/Access Token to assemble the full Facebook Graph URL
	page_id			=	auth['page_id']
	#access_token	=	getToken(APP_ID, APP_SECRET)
	access_token	=	auth['access_token']
	
	file = files['tweets']
	
	url_complete = "https://graph.facebook.com/v3.0/" + page_id + "/posts?access_token=" + access_token

	#prints the full URL for your convenience in the console if you want to follow or confirm the GRAPH response yourself
	print(url_complete)
	record.add(url_complete)

	#TODO: we get one more response than we fully use, debating on moving these checks into WriteResponseToFile
	reply = requests.get(url_complete)

	if reply.status_code > 399:
		record.add("Response: " + str(reply.status_code))
		return

	#200 status code doesn't mean a proper response
	if "error" in reply.json():
		record.add("Error Response")
		return

	#if its gotten this far, we can assume its a proper page json
	writeResponseToFile(file=file, key="data",url=url_complete, key2="paging", value="next")

def getToken(pAppID, pAppSecret):
  response = urllib.request.urlopen('https://graph.facebook.com/oauth/access_token?client_id=' +
    pAppID + '&client_secret=' + pAppSecret +
    '&grant_type=client_credentials')
  
  if response.getcode() == 200:
  	response = json.loads(response.read().decode('utf-8'))
  	return response["access_token"]
  else:
  	return None

def writeResponseToFile(file, key, url, **kwargs):
	with open(file, 'w+', encoding='utf-8') as f:
		f.write("{\n\t\"" + key +"\": [\n")
		
		while  url != "":
			reply = requests.get(url)
			json_string = reply.json()
			
			i = 0
			for message in json_string[key]:
				i += 1
				try:
					f.write(json.dumps(message, indent=True, ensure_ascii=False) + 
						(",", "")[i==len(json_string[key]) and kwargs['value'] not in json_string[kwargs['key2']]]
						#quick list that checks if this message is infact the last possible entry, therefore omits the comma
						#TODO: This bit of code here basically makes it not usable with anything but facebook GRAPH jsons
						#a bit more generic but still makes the assumption that there's going to be a second set of keys and values to check against
					)
				except KeyError as e:
					record.add(str(e))

			#iterate through the GRAPH response chain
			try:
				url = json_string[kwargs["key2"]][kwargs["value"]]
			except KeyError:
				record.add("Response chain end reached")
				break

		f.write("]\n\t}")
	f.close()
	record.add("Done")
	jsonloader.prettyPrint(file)

if __name__ == '__main__':
	#WARNING: Change this to the correct file path before running
	record = logging.log()
	defaultPath = "data/auth.hjson"

	try:
		j = jsonloader.loadHjson(sys.argv[1])
		record.add(str(sys.argv[1]) + " opened")
	except IndexError as e:
		j = jsonloader.loadHjson(defaultPath)
		record.add(defaultPath + " opened")

	facebookScrape(j)

	#Should I function this out? ¯\_(ツ)_/¯
	with open(j["files"]["logging"].replace("log", "facebooklog"), "w+", encoding='utf-8') as f:
		f.write(str(record.getLog()[0]) + "\n")
		for item in record.getLog()[1:]:
			f.write("\t" + str(item) + '\n')
		f.write("Logging Closed")
		f.close()

	exit()
