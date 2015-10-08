import os
import csv
import subprocess
from sys import argv

script, rootPath, symFile = argv

rootPath = os.path.normpath(rootPath)
with open(symFile, mode='r') as file:
	reader = csv.reader(file)
	logger = open('error.txt', 'w')
	for row in reader:
		if row[0] == 'Link':	# This is the title row
			continue
		symTo = os.path.normpath(row[0])
		toPath = os.path.join(rootPath, symTo)
		symFrom = os.path.normpath(row[1])
		fromPath = os.path.join(rootPath, symFrom)
		repo = symTo.split(os.path.sep)[1]
		repoPath = os.path.join(rootPath, repo)
		if not os.path.exists(toPath):
			logger.write('Link file not exists: ' + toPath + '\n')
			continue
		if not os.path.exists(fromPath):
			logger.write('Original file not exists: ' + fromPath + '\n')
			continue
		if repo == '3rdParty' or repo == 'BIWeb':
			# cd to repository
			os.chdir(repoPath)
			# rm the existing symlink file or directory
			subprocess.call(['git', 'rm', '-rf', toPath])
			subprocess.call(['cp', '-r', fromPath, toPath])
	logger.close()
	os.chdir(rootPath)
	subprocess.call(['repo', 'forall', '-c', 'git', 'add', '.'])
	subprocess.call(['repo', 'forall', '-c', 'git', 'commit', '-m', '"replace symlinks"'])