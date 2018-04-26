#!/usr/bin/python3
import sys
import os
import json
from urllib.request import urlopen

# if version_init != nouvelle_vers:
# 	save nouvelle_vers
# 	version_init = nouvelle_vers

device = ['iPhone5,4', 'iPad2,5', 'iPhone8,1', 'iPad2,1', 'iPad2,1']
ecid = ['294E20AC389', '2E1AA035DF3', '35CE921E2C', '1E0591EF58C', '278490E1D0C']

def download_json(url, filename):
	dl_file = urlopen(url)
	with open(filename, 'wb') as output:
		output.write(dl_file.read())

def parse_json(model, type):
	
	if type == "version": # latest version
		json_file = "firmwares.json"
		download_json("https://api.ipsw.me/v3/"+ model + "/latest/info.json", json_file)
		data = json.load(open(json_file))
		with open(json_file):
			ios_version = data[0]["version"]
		return ios_version
	
	elif type == "board":
		json_file = "board.json"
		download_json("https://api.ineal.me/tss/all/all", json_file)
		data = json.load(open("board.json"))
		board = data[model]["board"]
		return board

	else : 
		print("error")


def save_blobs(model, board_id, version, ecid):
	cmd = "tsschecker -d " + model + " -B " + board_id + " -i " + version + " -e " + ecid + " -s"
	os.system(cmd)

	# tsschecker_tool -d iPhone5,4 -i 10.3.3 -e 294E20AC389 -s
if __name__ == '__main__':
	# parse_json("iphone2,1")

	for i in range(0,len(device)):
		print("%s a pour ecid %s" % (device[i], ecid[i]))
		device_version = parse_json(device[i], "version")
		board_model    = parse_json(device[i], "board")
		save_blobs(device[i], board_model, device_version, ecid[i])
		
	# device_model = parse_json()