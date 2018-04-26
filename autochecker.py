#!/usr/bin/python3
import sys
import os
import json
from urllib.request import urlopen

# version_init = 10.3.2
# nouvelle_vers = 10.3.3

# if version_init != nouvelle_vers:
# 	save nouvelle_vers
# 	version_init = nouvelle_vers

# obtenir la dernière version
# ecid = {"xxxxxxx", "xxxxxxx"}
# device = {"iphonexx", "iphonexx"}


#for i in range(0,len(ecid)):
#	tss_save ecid[i]
device = ['iphone5,1', 'iPhone5,4', 'iPhone2,1', 'iPad2,1', 'iPhone10,1', 'iPod5,1', 'iPod6,1']
ecid = ['11111111', '22222222', '33333333', '33333333', '44444444', '55555555', '66666666', '7777777']

def download_json(url, filename):
	dl_file = urlopen(url)
	with open(filename, 'wb') as output:
		output.write(dl_file.read())

# parse_json("iphone5,4", "version")
# parse_json("iphone5,4", "board")

def parse_json(model, type):
	
	if type == "version": # latest version
		json_file = "firmwares.json"
		download_json("https://api.ipsw.me/v3/"+ model + "/latest/info.json", json_file)
		data = json.load(open(json_file))
		with open(json_file):
			ios_version = data[0]["version"]
			buildid = data[0]["buildid"]
			ipswfile = data[0]["filename"]
			url = data[0]["url"]
			size = data[0]["size"]
		print(ios_version)
	
	elif type == "board":
		json_file = "board.json"
		download_json("https://api.ineal.me/tss/all/all", json_file)
		data = json.load(open("board.json"))
		print(data[model]["board"])

	else : 
		print("error")

if __name__ == '__main__':
	# parse_json("iphone2,1")

	parse_json("iphone5,4", "version")
	parse_json("iPhone5,4", "board")
	#for i in range(0,len(device)):
	#	print("%s a pour ecid %s" % (device[i], ecid[i]))
