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
			repo = symlinkPath.split(rootPath)[1].split('/')[1]
			os.chdir(os.path.join(rootPath, repo))
			#subprocess.call(['pwd'])
			subprocess.call(['git', 'rm', symlinkPath])
			subprocess.call(['cp', originalPath, symlinkPath])
		subprocess.call(['repo', 'forall', '-c', 'git', 'add', '.'])
		subprocess.call(['repo', 'forall', '-c', 'git', 'commit', '-m', '"replace symlinks"'])

	def getSymlinksMap(self, rootPath):
		print "========================================= Getting symlink and original from repositories"
		self.rootPath = rootPath
		repos = os.listdir(rootPath)
		for repo in repos:
			repoPath = os.path.join(rootPath, repo)
			# Ignore those non-git directories
			if os.path.isdir(os.path.join(repoPath, '.git')):
				symlinks = self.findSymlinks(repoPath)
				for symlink in symlinks:
					symlinkPath = os.path.join(repoPath, symlink)
					originalPath = self.getOriginalPath(repo, symlinkPath)
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
			paths = path.split('../')
			if paths[-1].startswith('BIWebSDK') or paths[-1].startswith('BIWebApp'):
				paths[-1] = 'BIWeb/' + paths[-1]
			elif paths[-1].startswith('COM') or paths[-1].startswith('Common') or paths[-1].startswith('Engine') or paths[-1].startswith('Kernel'):
				paths[-1] = 'Server/' + paths[-1]
			originalPath = os.path.join(self.rootPath, paths[-1])
		return originalPath

	def findSymlinks(self, repoPath):
		os.chdir(repoPath)
		proc1 = subprocess.Popen(['git', 'ls-files', '-s'], stdout=subprocess.PIPE)
		proc2 = subprocess.Popen(['egrep', '^120000'], stdin=proc1.stdout, stdout=subprocess.PIPE)
		infoList = proc2.communicate()[0].split()
		files = []
		for i in range(3, len(infoList), 4):
			files.append(infoList[i])
		return files