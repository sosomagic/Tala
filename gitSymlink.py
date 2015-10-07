import os
import subprocess
import csv
from gitSymlink import *
from sys import argv

class gitSymlink(object):
	symlinkDict = {}
	rootPath = ''

	def replaceSymlinks(self, rootPath):
		self.rootPath = rootPath
		for symlinkPath, originalPath in self.symlinkDict.iteritems():
			if not originalPath or not os.path.exists(originalPath) or not os.path.exists(symlinkPath):
				continue
			repo = symlinkPath.split(rootPath)[1].split('\\')[0]
			#print os.path.join(rootPath, repo)
			#y = raw_input("continue?")
			os.chdir(os.path.join(rootPath, repo))
			#subprocess.call(['pwd'])
			subprocess.call(['git', 'rm', '-rf', symlinkPath])
			subprocess.call(['cp', '-r', originalPath, symlinkPath])
		subprocess.call(['repo', 'forall', '-c', 'git', 'add', '.'])
		subprocess.call(['repo', 'forall', '-c', 'git', 'commit', '-m', '"replace symlinks"'])

	def getSymlinksMap(self, rootPath):
		print "========================== Getting symlink and original from repositories =========================="
		self.rootPath = os.path.normpath(rootPath)
		repos = os.listdir(rootPath)
		for repo in repos:
			if repo == 'Mobile':
				continue
			repoPath = os.path.join(rootPath, repo)
			# Ignore those non-git directories
			if os.path.isdir(os.path.join(repoPath, '.git')):
				symlinks = self.findSymlinks(repoPath)
				#print symlinks
				for symlink in symlinks:
					symlinkPath = os.path.join(repoPath, symlink)
					symlinkPath = os.path.normpath(symlinkPath)
					if os.path.exists(symlinkPath):
						originalPath = self.getOriginalPath(repo, symlinkPath)
						symlinkPath = os.path.normpath(symlinkPath)
						if originalPath and os.path.exists(originalPath):
							self.symlinkDict[symlinkPath] = originalPath
							print symlinkPath, originalPath
		#self.writeSymlinkDicttoFile(rootPath + '/dict1.csv')
		for key, value in self.symlinkDict.iteritems():
			n = 0
			while self.symlinkDict.has_key(value) and n < 10:
				self.symlinkDict[key] = self.symlinkDict[value]
				value = self.symlinkDict[key]
				print value
				n += 1
			if n == 10:
				print "There is infinite loop for the nested symlinks"
		self.writeSymlinkDicttoFile(rootPath + '/dict.csv')

	def printSymlinkDict(self):
		for key, value in self.symlinkDict.iteritems():
			print "symlink:  " + key
			print "original: " + value
			print "+++++++++++++++++++++++++++++"

	def writeSymlinkDicttoFile(self, filename):
		with open(filename, 'w') as f:
			fieldnames = ['symlink', 'original']
			writer = csv.writer(f)
			for key, value in self.symlinkDict.iteritems():
				writer.writerow([key, value])

	def getOriginalPath(self, repo, symlinkPath):
		with file(symlinkPath) as f:
			path = ''
			originalPath = ''
			try:
				path = f.read()
			except:
				print "open error: " + symlinkPath
			if not path:
				print 'invalid symlink'
				return
		return self.restoreAbsPath(symlinkPath, path)

	def restoreAbsPath(self, curPath, relPath):
		originalPath = None
		sep = os.path.sep
		curPath = os.path.normpath(curPath)
		relPath = os.path.normpath(relPath)
		#print 'curPath: ' + curPath
		#print 'relPath: ' + relPath
		relPath = '..' + sep + '..' + sep + relPath
		tmpPath = os.path.normpath(curPath+relPath)
		#print 'tmpPath: ' + tmpPath
		oriRef = relPath.split('..'+sep)[-1].split(sep)[0]
		oriRepo = os.path.split(tmpPath.split(sep+relPath.split('..'+sep)[-1])[0])[1]
		
		if oriRepo == 'BIWeb' and (oriRef == 'BIWebApp' or oriRef == 'BIWebSDK'):
		 	originalPath = os.path.normpath(os.path.join(self.rootPath, 'BIWeb', relPath.split('..'+sep)[-1]))
		elif oriRepo == 'Server' and (oriRef == 'Common' or oriRef == 'COM' or oriRef == 'Engine' or oriRef == 'Kernel'):
			originalPath = os.path.normpath(os.path.join(self.rootPath, 'Server', relPath.split('..'+sep)[-1]))
		else:
			originalPath = tmpPath
		#print 'originalPath: ' + originalPath
		return os.path.normpath(originalPath)

	def findSymlinks(self, repoPath):
		os.chdir(repoPath)
		proc1 = subprocess.Popen(['git', 'ls-files', '-s'], stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(['egrep', '^120000'], stdin=proc1.stdout, stdout=subprocess.PIPE)
		proc3 = subprocess.Popen(['cut', '-f', '2'], stdin=proc2.stdout, stdout=subprocess.PIPE)
		infoList = proc3.communicate()[0].split('\r\n')
		files = []
		for i in infoList:
			if i:
				files.append(os.path.normpath(i))
		return files

if __name__ == '__main__':
	script, view_path = argv
	gitSymlink().getSymlinksMap(view_path)
	#gitSym.replaceSymlinks(view_path)