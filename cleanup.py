#This script is to delete all files and directories created old than a given days.
#This is a solution for usher build server, I will deploy this script to the server and run a periodical cleanup
from sys import argv
from subprocess import call

script, file_path, days_older_than = argv

call(["find", file_path, "-mtime", "+"+days_older_than, "-exec", "rm", "-rf", "{}", "\\", ";"])

