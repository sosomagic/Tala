from sys import argv
import subprocess
import os
import datetime
import string
import re

#ask file_path, where you want to do the cleanup as the argv
script, file_path = argv

buildDirList = os.listdir(file_path)

for buildDir in buildDirList:
	dirPath = os.path.join(file_path, buildDir)
	if os.path.isdir(dirPath):
		latest_date = '00000000'
		latest_build = '0'
		latest_dir = ''
		print "We are dealing with: " + os.path.join(dirPath)
		dirList = os.listdir(dirPath)
		for dir in dirList:
			if (re.match('\A\d\d\d\d\d\d\d\d_\d{0,4}', dir)) and os.path.isdir(os.path.join(dirPath, dir)):
				strs = dir.split('_')
				date = strs[0]
				buildNum = strs[1]
				if date > latest_date:
					latest_dir = dir
				elif date == latest_date:
					if buildNum > latest_build:
						latest_dir = dir
		if latest_dir:		
			source = os.path.join(dirPath, latest_dir)
			destination = os.path.join(dirPath, 'Latest')
			
			if not os.path.exists(destination):
				subprocess.call(['cp', '-r', source, destination])
				print "copy " + source + " to " + destination
			else:
				print destination + " exists"
		else:
			print "no build is found in this directory"
