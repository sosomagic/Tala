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
	relativePath = ''
	with file(symlink) as f:
		relativePath = f.read()
	print "path read from file is: " + relativePath
	# This is an invalid symlink file, just remove it
	if not relativePath: 
		subprocess.call(['git', 'rm', symlink])
		return
	if repo == 'BIWeb' or repo == 'Server':
	 	# BIWebApp and BIWebSDK have been combined into one repository BIWeb
		print 'BIWeb'
	elif repo == 'Server':
	 	# COM, Common, Engine and Kernel have been combined into one repository Server
		print 'Server'
	else:
	 	# For all others repository, the relative path should be retained as in ClearCase
	 	origFilePath = os.path.abspath(path)
		# If the original file doesn't exist, this symlink is invalid and just remove it
		if not os.path.isfile(origFilePath):
			subprocess.call(['git', 'rm', symlink])
			return
		print "copying " + origFilePath + " to " + symlinkPath
		subprocess.call(['git', 'rm', symlink])
		subprocess.call(['cp', origFilePath, './'])
		subprocess.call(['git', 'add', symlink])
		subprocess.call(['git', 'commit', '-m', '"replace symlink"'])


for repo in repos:
	repoPath = os.path.join(view_path, repo)
	if os.path.isdir(os.path.join(repoPath, '.git')):
		symlinks = findSymlinks(repoPath)
		while symlinks:
			print symlinks
			#resolve symlinks
			for symlink in symlinks:
				print "find symlink: " + repo + '/' + symlink
				replaceSymlinkbyFile(repo, symlink)
			#find again to resolve the embeded symlinks
			symlinks = findSymlinks(repoPath)


