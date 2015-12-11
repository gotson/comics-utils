from struct import unpack
import os
import shutil
from datetime import datetime
import subprocess

def getTags(f):
	return filter(None,subprocess.check_output(["/usr/local/bin/tag","-Ng",f]).split('\n'))


root = '/Books/'
syncdir = '/Books/_sync/'
size = 0
count = 0

# clean destination
for the_file in os.listdir(syncdir):
    file_path = os.path.join(syncdir, the_file)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except:
        pass
if not os.path.exists(syncdir):
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
	else:
		relpath = os.path.relpath(dirpath,root)
		destdir = os.path.join(syncdir,relpath)
		for file in files:
			filepath = os.path.join(dirpath, file)
			if 'sync' in getTags(filepath):
				if not os.path.exists(destdir):
					os.makedirs(destdir)
				os.link(filepath,os.path.join(destdir,file))
				size += os.path.getsize(filepath)
				count += 1

print '{} {} files linked, total {} bytes'.format(datetime.now(),count,size)
