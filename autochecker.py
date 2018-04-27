#!/usr/bin/python3
import sys
import os
import json
from urllib.request import urlopen

device_list = list()
ecid_list = list()

# function to download json files
def download_json(url, filename):
	dl_file = urlopen(url)
	with open(filename, 'wb') as output:
		output.write(dl_file.read())

# function to parse json files.
# we parse firmwares.json and board.json
# the last one is just to get the board id for tsschecker
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

# simple function to save blobs by calling tsschecker
def save_blobs(model, board_id, version, ecid):
	save_dir = "shsh2"
	cmd = "tsschecker -d " + model + " -B " + board_id + " -i " + version + " -e " + ecid + " -s --save-path " + save_dir
	try :
		os.stat(save_dir)
	except:
		os.mkdir(save_dir)
	os.system(cmd)

def usage(name):
	print("usage: %s [config file]" % name)

if __name__ == '__main__':
	argv = sys.argv
	argc = len(sys.argv)

	if argc != 2:
		usage(argv[0])
		sys.exit(1)

	if not os.path.isfile(argv[1]):
		print("%s : file not found" % argv[1])
		sys.exit(1)
	else :
		config_file = argv[1]

	with open(config_file) as f:
		content = f.readlines()
		for i in range(0, len(content)):
			type = content[i].split(' ')[0]
			if type == "[device]":
				device = content[i].split(' ')[1]
				device = device.split('\n')[0]
				device_list.append(device)
			elif type == "[ecid]" :
				ecid = content[i].split(' ')[1]
				ecid = ecid.split('\n')[0]
				ecid_list.append(ecid)

	for i in range(0,len(device_list)):
		print("%s a pour ecid %s" % (device_list[i], ecid_list[i]))
		device_version = parse_json(device_list[i], "version")
		board_model    = parse_json(device_list[i], "board")
		save_blobs(device_list[i], board_model, device_version, ecid_list[i])