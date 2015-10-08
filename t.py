import os
import csv

print os.path.exists('/BIWeb/BIWebApp/code/html/MSTRWeb/WEB-INF')

rootPath = '~/tmp/'

with open('result.csv', mode='r') as file:
	reader = csv.reader(file)
	logger = open('error.txt', 'w')
	for row in reader:
		if row[0] == 'Link':	# This is the title row
			continue
		symTo = os.path.normpath(row[0])
		toPath = os.path.join(rootPath, symTo)
		symFrom = os.path.normpath(row[1])
		fromPath = os.path.join(rootPath, symFrom)
		if symFrom.startswith(os.path.normpath('/BIWeb/BIWebApp/code/html/MSTRWeb/WEB-INF')):
			print fromPath
			print os.path.exists(fromPath)