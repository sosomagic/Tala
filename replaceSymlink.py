import os
import csv
import subprocess
import shutil
from sys import argv

script, rootPath, symFile = argv

rootPath = os.path.normpath(rootPath)

def copyanything(fromPath, toPath):
	head = os.path.split(toPath)[0]
	tail = os.path.split(toPath)[1]
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
		if repo == '3rdParty_UNIX' or repo == 'Systools_UNIX':
			continue
		
		if not os.path.exists(toPath):
			continue
		if os.path.exists(fromPath):
			# cd to repository
			os.chdir(repoPath)
			# rm the existing symlink file or directory
			subprocess.call(['git', 'rm', '-rf', toPath])
			copyanything(fromPath, toPath)
		else:
			print fromPath + 'write into log'
			logger.write('Original file not exists: ' + fromPath + '\n')
	logger.close()

repos = os.listdir(rootPath)
for repo in repos:
	repoPath = os.path.join(rootPath, repo)
	if os.path.isdir(os.path.join(repoPath, '.git')):
		if os.path.exists(repoPath):
			os.chdir(repoPath)
			subprocess.call(['git', 'add', '.'])
			subprocess.call(['git', 'commit', '-m', '"replace symlinks"'])