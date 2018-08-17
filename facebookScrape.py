#!/usr/bin/env python3

import requests, urllib, warnings, json
from custompackages import jsonloader

def main():
	
	d = jsonloader.loadJson("data/auth.json")
	
	assert(d), "File does not exist."

	auth = d['auth']
	files = d['files']

	#TODO: These do nothing. Remove?
	#APP_ID 		=	auth['app_id']
	#APP_SECRET 	=	auth['app_secret']

	#These pull the Page id/Access Token to assemble the full Facebook Graph URL
	page_id			=	auth['page_id']
	access_token	=	auth['access_token']
	
	file = files['tweets']
	url_complete = "https://graph.facebook.com/v3.0/" + page_id + "/posts?access_token=" + access_token
	
	print(url_complete)

	#TODO: we get one more response than we fully use, debating on moving these checks into WriteResponseToFile
	reply = requests.get(url_complete)

	if reply.status_code > 399:
		print("Response: " + str(reply.status_code))
		return

	#200 status code doesn't mean a proper response
	if "error" in reply.json():
		print("Error Response")
		return

	#if its gotten this far, we can assume its a proper page json
	writeResponseToFile(file=file, key="data",url=url_complete, key2="paging", value="next")



def writeResponseToFile(file, key, url, **kwargs):
	with open(file, 'w+', encoding='utf-8') as f:
		f.write("{\n\t\"" + key +"\": [\n")
		while  url != "":
			reply = requests.get(url)
			json_string = reply.json()

			i = 0
			for message in json_string[key]:
				i += 1
				
				f.write(json.dumps(message, indent=True, ensure_ascii=False) + 
					(",", "")[i==len(json_string[key]) and kwargs['value'] not in json_string[kwargs['key2']]]
					#quick list that checks if this message is infact the last possible entry, therefore omits the comma
					#TODO: This bit of code here basically makes it not usable with anything but facebook GRAPH jsons
					#a bit more generic but still makes the assumption that there's going to be a second set of keys and values to check against
				)

			#iterate through the GRAPH response chain
			try:
				url = json_string[kwargs["key2"]][kwargs["value"]]
			except KeyError:
				break

		f.write("]\n\t}")
	f.close()
	jsonloader.prettyPrint(file)

if __name__ == '__main__':
	main()

