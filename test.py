from sys import argv
import subprocess
import os
import datetime
import string
import re

#ask file_path, where you want to do the cleanup as the argv
script, file_path = argv

cleanup_date = (datetime.date.today() - datetime.timedelta(days=10)).strftime('%Y%m%d')
print "I will delete the build files older than 2 months, but I will keep the latest build for each milestone."

find_dir = False

for dirname, dirnames, filenames in os.walk(file_path):
	for dir in dirnames:
		if (re.match('\A\d\d\d\d\d\d\d\d_\d{0,4}', dir)):	
			#print os.path.join(dirname,dir)
			if cleanup_date > dir[0:8]:
				dir_del = os.path.join(dirname, dir)
				print dir_del
				#subprocess.call(['rm', '-rf', dir_del])
