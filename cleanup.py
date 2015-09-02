#This script is to delete all files and directories created old than a given days.
#This is a solution for usher build server, I will deploy this script to the server and run a periodical cleanup
from sys import argv
import subprocess

script, file_path, days_older_than = argv
#This is using xargs command and PIPE
files = subprocess.Popen(["find", file_path, "-mtime", "+"+days_older_than, "-print0"], stdout=subprocess.PIPE)
subprocess.Popen (["xargs", "-0", "rm", "-rf"], stdin=files.stdout)

#This is using -exec command
#subprocess.call(["find", file_path, "-mtime", "+"+days_older_than, "-exec", "rm", "-rf", "{}", "\\", ";"])

