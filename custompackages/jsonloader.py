#!/usr/bin/python3

import json, hjson

def loadJson(filename, encoding='utf-8'):
	#returns a json file as a python object
	try:
		with open(filename, "r", encoding=encoding) as f:
			data = f.read()
		f.close()
	except FileNotFoundError as e:
		print(e + ": " + filename)
		return None
	return json.loads(data)

def loadHjson(filename, encoding='utf-8'):
	#returns a hjson file as a python object
	try:
		with open(filename, "r", encoding=encoding) as f:
			data = f.read()
		f.close()
	except FileNotFoundError as e:
		print(e)
		return None
	return hjson.loads(data)

def prettyPrint(filename, encoding='utf-8'):
	pretty = loadJson(filename)
	with open(filename, 'w+', encoding=encoding) as f:
		f.write(json.dumps(pretty, indent=True))
	f.close()
