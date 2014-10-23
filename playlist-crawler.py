#!/usr/bin/env python
import os, sys, subprocess

# Default settings
path = '/home/medlem/divskrot/flim/Electronica'
url = 'http://www.youtube.com/playlist?list=PLFPg_IUxqnZM3uua-YwStHJ1qmlQKBnh0'

if (len(sys.argv) > 2):
	# minimum two input-arguments after script name - optional output path
	path = sys.argv[2]
	url = sys.argv[1]

elif (len(sys.argv) > 1):
	if sys.argv[1] is '-h' or '--help' or '--usage':
		exit("Simple script to keep a local folder in sync with a youtube playlist...\n\nUse: playlist-crawler.py [url] [path]\n	url:	can be video or playlist, default 'YouTube Top 100 Electronica playlist'\n	path:	Where to store downloaded videos, default: '"+path+"'\n\nBoth default variables are configurable, can be edited at the top of the file - enjoy!")
	# Assuming first argument to be playlist-url
	url = sys.argv[1]

tmpfile = '/tmp/ytcrawl'
command = "youtube-dl -ie --get-id "+url+" 1> "+tmpfile

#if os.system(command) is not 0:
#	sys.exit("System command returned value different from 0")

os.system(command)

def archive(filename):
	cmd = 'cd '+path+' && mkdir -p archived && mv "'+filename+'" archived/'
	if os.system(cmd) is not 0:
		print('Failed to archive '+filename)
		return False
	return True

files = os.listdir(path)
download = []
archived = []

listfile = open(tmpfile, 'r')

URL = False
temp_name = ''
vidlist = dict()
#print(vidlist_list)
for line in listfile:
	if URL is True:
		vidlist[temp_name] = line.rstrip()
	else:
		temp_name = line.rstrip()
		if not any(temp_name in filename for filename in files):
			download.append(temp_name)
	URL = not URL

# Find files to delete
for existing in files:
	if not any(name in existing for name in vidlist.keys()):
		if not 'archived' in existing:
			archived.append(existing)
			archive(existing)


#print(vidlist)
print("To be downloaded:")
print(download)
print("Files archived:")
print(archived)

for url in download:
	cmd = 'cd '+path+' && youtube-dl http://youtube.com/watch?v='+vidlist[url]
#	print(cmd)
	os.system(cmd)

#for file in files:
#	print(file)


