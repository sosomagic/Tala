import os
import subprocess
import csv

class gitSymlink(object):
	symlinkDict = {}
	rootPath = ''

	def replaceSymlinks(self, rootPath):
		self.rootPath = rootPath
		for symlinkPath, originalPath in self.symlinkDict.iteritems():
			if not originalPath or not os.path.exists(originalPath):
				continue
			repo = symlinkPath.split(rootPath)[1].split('\\')[0]
			print os.path.join(rootPath, repo)
			y = raw_input("continue?")
			os.chdir(os.path.join(rootPath, repo))
			#subprocess.call(['pwd'])
			subprocess.call(['git', 'rm', '-rf', symlinkPath])
			subprocess.call(['cp', '-r', originalPath, symlinkPath])
		subprocess.call(['repo', 'forall', '-c', 'git', 'add', '.'])
		subprocess.call(['repo', 'forall', '-c', 'git', 'commit', '-m', '"replace symlinks"'])

	def getSymlinksMap(self, rootPath):
		print "========================================= Getting symlink and original from repositories"
		self.rootPath = rootPath
		repos = os.listdir(rootPath)
		for repo in repos:
			if repo == 'Mobile':
				continue
			repoPath = os.path.join(rootPath, repo)
			# Ignore those non-git directories
			if os.path.isdir(os.path.join(repoPath, '.git')):
				symlinks = self.findSymlinks(repoPath)
				for symlink in symlinks:
					symlinkPath = os.path.join(repoPath, symlink).replace('/', '\\')
					originalPath = self.getOriginalPath(repo, symlinkPath).replace('/', '\\')
					if originalPath:
						self.symlinkDict[symlinkPath] = originalPath
					#print "symlink: " + symlinkPath
					#print "original: " + originalPath
		# Resolve the nested symlink pointer
		#self.printSymlinkDict()
		#self.writeSymlinkDicttoFile(rootPath + '/dict1.csv')
		for key, value in self.symlinkDict.iteritems():
			n = 0
			while self.symlinkDict.has_key(value) and n < 10:
				print key, value
				self.symlinkDict[key] = self.symlinkDict[value]
				value = self.symlinkDict[value]
				n += 1
			if n == 10:
				print "There is infinite loop for the nested symlinks"
		#self.printSymlinkDict()
		self.writeSymlinkDicttoFile(rootPath + '/dict2.csv')

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
		sep = None
		if relPath.startswith('../'):
			sep = '/'
		else:
			sep = '\\'
		paths = relPath.split(sep)
		curPath = os.path.abspath(os.path.join(curPath, os.pardir))
		for path in paths:
			if path == '..':
				curPath = os.path.abspath(os.path.join(curPath, os.pardir))
			else:
				break
		paths = relPath.split('..' + sep)
		if paths[-1].startswith('BIWebSDK') or paths[-1].startswith('BIWebApp'):
			curPath = os.path.abspath(os.path.join(curPath, os.pardir))
			paths[-1] = 'BIWeb/' + paths[-1]
		elif paths[-1].startswith('COM') or paths[-1].startswith('Common') or paths[-1].startswith('Engine') or paths[-1].startswith('Kernel'):
			curPath = os.path.abspath(os.path.join(curPath, os.pardir))
			paths[-1] = 'Server/' + paths[-1]
		return os.path.join(curPath, paths[-1])

	def findSymlinks(self, repoPath):
		os.chdir(repoPath)
		proc1 = subprocess.Popen(['git', 'ls-files', '-s'], stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(['egrep', '^120000'], stdin=proc1.stdout, stdout=subprocess.PIPE)
		proc3 = subprocess.Popen(['cut', '-f', '2'], stdin=proc2.stdout, stdout=subprocess.PIPE)
		infoList = proc3.communicate()[0].split('\r\n')
		files = []
		for i in infoList:
			if i:
				files.append(i)
		return files
