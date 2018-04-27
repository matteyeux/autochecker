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

def save_info(model, ecid, version):
	f = open('latest_version.txt', 'a')
	device_info = "[device] " + model + "\n"
	ecid_info = "[ecid] " + ecid + "\n"
	version_info = "[version] " + version + "\n\n"
	f.write(device_info)
	f.write(ecid_info)
	f.write(version_info)
	f.close()

def isNewVersion(model, ecid, version):
	device2check = ""
	version2check = ""
	if not os.path.isfile("latest_version.txt"):
		return True

	with open("latest_version.txt") as f:
		line  = f.readlines()
		for i in range(0, len(line)):
			check = line[i].split(' ')[0]
			if check == "[device]":
				device2check = line[i].split(' ')[1]
				device2check = device2check.split('\n')[0]
				#print(device2check)
			elif check == "[ecid]" :
				ecid2check = line[i].split(' ')[1]
				ecid2check = ecid2check.split('\n')[0]
				#print(ecid2check)
			elif check == "[version]" :
				version2check = line[i].split(' ')[1]
				version2check = version2check.split('\n')[0]
				#print(version2check)

			if model == device2check and version == version2check and ecid == ecid2check:
				return False # same version

		return True

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
		device_version = parse_json(device_list[i], "version")
		board_model    = parse_json(device_list[i], "board")
		if isNewVersion(device_list[i], ecid_list[i], device_version) == True:
			save_info(device_list[i], ecid_list[i], device_version)
			save_blobs(device_list[i], board_model, device_version, ecid_list[i])
		else:
			print("[i] SHSH2 for %s on %s already exists" % (device_list[i], device_version))