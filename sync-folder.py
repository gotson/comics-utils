from xattr import xattr
from struct import unpack
import os
import shutil
from datetime import datetime
import subprocess

# xattr solution
def getColor(f):
	try:
	    attrs = xattr(f)
	    finder_attrs = attrs[u'com.apple.FinderInfo']
	    flags = unpack(32*'B', finder_attrs)
	    color = flags[9] >> 1 & 7
	except KeyError:
	    color = 0
	return colornames[color]
colornames = { 0: 'none', 1: 'gray', 2 : 'green', 3 : 'purple', 4 : 'blue', 5 : 'yellow', 6 : 'red', 7 : 'orange' }
# end

def getTags(f):
	return filter(None,subprocess.check_output(["/usr/local/bin/tag","-Ng",f]).split('\n'))


root = '/Books/'
syncdir = '/Books/_sync/'
size = 0
count = 0

# clean destination
try:
	shutil.rmtree(syncdir)
except:
	pass
os.makedirs(syncdir)

# list of dirs to sync, to check against children to avoid having to tag children folders
lDirSync=[]

for dirpath, folders, files in os.walk(root):
	files = [f for f in files if not f[0] == '.']
	bSync = False
	#check for parents with 'sync' tag
	for p in lDirSync:
		if os.path.commonprefix([os.path.dirname(dirpath),p]) == p:
			bSync = True
	#if getColor(dirpath) == 'blue':
	if 'sync' in getTags(dirpath):
		lDirSync.append(dirpath)
		bSync = True
	if bSync:
		# replicate directory structure
		relpath = os.path.relpath(dirpath,root)
		destdir = os.path.join(syncdir,relpath)
		for file in files:
			filepath = os.path.join(dirpath, file)
			#if getColor(filepath) != 'gray':
			if 'read' not in getTags(filepath):
				if not os.path.exists(destdir):
					os.makedirs(destdir)
				os.link(filepath,os.path.join(destdir,file))
				size += os.path.getsize(filepath)
				count += 1

print '{} {} files linked, total {} bytes'.format(datetime.now(),count,size)
