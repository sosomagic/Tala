from sys import argv
import subprocess
import os

script, view_path = argv

# view_path need to be a full path, rather than a relative path
repos = os.listdir(view_path)

def findSymlinks(dirPath):
	os.chdir(dirPath)
	proc1 = subprocess.Popen(['git', 'ls-files', '-s'], stdout=subprocess.PIPE)
	proc2 = subprocess.Popen(['egrep', '^120000'], stdin=proc1.stdout, stdout=subprocess.PIPE)
	infoList = proc2.communicate()[0].split()
	files = []
	for i in range(3, len(infoList), 4):
		files.append(infoList[i])
	return files

def replaceSymlinkbyFile(repo, symlink):
	repoPath = os.path.join(view_path, repo)
	os.chdir(repoPath)
	symlinkPath = os.path.join(repoPath, symlink)
	subprocess.Popen(['cat', symlinkPath])
	#origFilePath = 
	# if repo == 'BIWeb':
	# 	# BIWebApp and BIWebSDK have been combined into one repository BIWeb
	# elif repo == 'Server':
	# 	# COM, Common, Engine and Kernel have been combined into one repository Server
	# else:
	# 	# For all others repository, the relative path should be retained as in ClearCase


for repo in repos:
	repoPath = os.path.join(view_path, repo)
	if os.path.isdir(os.path.join(repoPath, '.git')):
		symlinks = findSymlinks(repoPath)
		while symlinks:
			#resolve symlinks
			for symlink in symlinks:
				replaceSymlinkbyFile(repo, symlink)
			#find again to resolve the embeded symlinks
			symlinks = findSymlinks(repoPath)


