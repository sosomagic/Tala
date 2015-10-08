import os
import csv
import subprocess
from sys import argv

script, rootPath, symFile = argv

rootPath = os.path.normpath(rootPath)
with open(symFile, mode='r') as file:
	reader = csv.reader(file)
	for row in reader:
		if row[0] == 'Link':	# This is the title row
			continue
		symTo = os.path.normpath(row[0])
		toPath = os.path.join(rootPath, symTo)
		symFrom = os.path.normpath(row[1])
		fromPath = os.path.join(rootPath, symFrom)
		repo = symTo.split(os.path.sep)[1]
		repoPath = os.path.join(rootPath, repo)
		# cd to repository
		os.chdir(repoPath)
		# rm the existing symlink file or directory
		subprocess.call(['git', 'rm', '-rf', symToPath])
		subprocess.call(['cp', '-r', symFromPath, symToPath])
		