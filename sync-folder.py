from struct import unpack
import os
import shutil
from datetime import datetime
import subprocess
import filecmp

def getTags(f):
	return filter(None,subprocess.check_output(["/usr/local/bin/tag","-Ng",f]).split('\n'))


root = '/Books/'
syncdir = '/Books/_sync/'

READ = 'read'
SYNC = 'sync'

# list of dirs to sync, to check against children to avoid having to tag children folders
lDirSync=[]
# list of dirs read, to check against children to avoid having to tag children folders
lDirRead=[]
# list of files to sync, in a tuple form (source, destination)
lSync=[]
# list of existing files in destination folder
lExist=[]

# list existing files
for dirpath, folders, files in os.walk(syncdir):
	folders[:] = [d for d in folders if d not in '.sync']
	files = [f for f in files if not f[0] == '.']
	for f in files:
		lExist.append(os.path.join(dirpath,f))

# go through source
for dirpath, folders, files in os.walk(root):
	files = [f for f in files if not f[0] == '.']
	# skip 'read' directories completely
	if READ in getTags(dirpath):
		lDirRead.append(dirpath)
		continue
	bSync = False
	# check for parents with 'sync' tag
	for p in lDirSync:
		if os.path.commonprefix([os.path.dirname(dirpath),p]) == p:
			bSync = True
	for p in lDirRead:
		if os.path.commonprefix([os.path.dirname(dirpath),p]) == p:
			bSync = False
	if SYNC in getTags(dirpath):
		lDirSync.append(dirpath)
		bSync = True
	if bSync:
		# replicate directory structure
		relpath = os.path.relpath(dirpath,root)
		destdir = os.path.join(syncdir,relpath)
		for file in files:
			filepath = os.path.join(dirpath, file)
			if READ not in getTags(filepath):
				if not os.path.exists(destdir):
					print "Adding directory: {}".format(destdir)
					os.makedirs(destdir)
				filepathdest = os.path.join(destdir,file)
				lSync.append((filepath, filepathdest))
	else:
		relpath = os.path.relpath(dirpath,root)
		destdir = os.path.join(syncdir,relpath)
		for file in files:
			filepath = os.path.join(dirpath, file)
			if SYNC in getTags(filepath):
				if not os.path.exists(destdir):
					os.makedirs(destdir)
				filepathdest = os.path.join(destdir,file)
				lSync.append((filepath, filepathdest))

# compare source and destination
for source, dest in lSync:
	if dest in lExist:
		if not filecmp.cmp(source, dest):
			print "Replacing: {}".format(dest)
			os.remove(dest)
			os.link(source, dest)
		lExist.remove(dest)
	else:
		print "Adding: {}".format(dest)
		os.link(source, dest)

for f in lExist:
	print "Removing: {}".format(f)
	os.remove(f)

for dirpath, folders, files in os.walk(syncdir):
	folders[:] = [d for d in folders if d not in '.sync']
	if not folders and not files:
		print "Removing directory: {}".format(dirpath)
		os.rmdir(dirpath)
