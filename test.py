from sys import argv
import subprocess
import os
from gitSymlink import *

script, view_path = argv

gitSym = gitSymlink()
gitSym.getSymlinksMap(view_path)
gitSym.replaceSymlinks(view_path)