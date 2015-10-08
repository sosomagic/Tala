import os
import csv
import subprocess
import shutil
from sys import argv

script, rootPath, symFile = argv

rootPath = os.path.normpath(rootPath)

def copyanything(fromPath, toPath):
	head = toPath.split()[0]
	tail = toPath.split()[1]
	if not os.path.exists(head):
		os.makedirs(head)
	if os.path.isdir(fromPath):
		shutil.copytree(fromPath, toPath)
	else:
		shutil.copy(fromPath, toPath)

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
		if repo == 'BIWeb':
			if os.path.exists(fromPath):
				# cd to repository
				os.chdir(repoPath)
				# rm the existing symlink file or directory
				subprocess.call(['git', 'rm', '-rf', toPath])
				copyanything(fromPath, toPath)
			else:
				print 'write into log'
				logger.write('Original file not exists: ' + fromPath + '\n')
	logger.close()
	os.chdir(rootPath)
	subprocess.call(['repo', 'forall', '-c', 'git', 'add', '.'])
	subprocess.call(['repo', 'forall', '-c', 'git', 'commit', '-m', '"replace symlinks"'])