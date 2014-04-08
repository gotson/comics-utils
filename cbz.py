import os
import shutil
import subprocess
from natsort import natsorted
import argparse
import logging
import tempfile
import zipfile

# unpack archive in temporary folder and return folder reference 
def unpack(f):
    tmpdir = tempfile.mkdtemp()
    tmp.append(tmpdir)
    p = subprocess.Popen(['/usr/local/bin/unar','-o',tmpdir,f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    
    if stdout:
        logger.info(stdout)
    if stderr:
        logger.error(stderr)
    return tmpdir

# cleanup all temporary folders created
def cleanup():
    for f in tmp:
        shutil.rmtree(f)

def getTags(f):
    return subprocess.check_output(['/usr/local/bin/tag','-lN',f]).rstrip()

def setTags(f,tags):
    p = subprocess.Popen(['/usr/local/bin/tag','-s',tags,f], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    
    if stdout:
        logger.info(stdout)
    if stderr:
        logger.error(stderr)

def zipFile(src, dst, junk, natural):
    zf = zipfile.ZipFile('{}'.format(dst), 'w', zipfile.ZIP_STORED)
    logger.info('Zipping content of {} inside: {}'.format(src,dst))
    for dirname, _, files in os.walk(src):
        # ignore hidden files
        files = [f for f in files if not f[0] == '.']
        i = 1
        if natural:
            files = natsorted(files, number_type=None)
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            if natural:
                _,ext = os.path.splitext(filename)
                filename = '{:04d}{}'.format(i,ext)
                i = i+1
            if junk:
                arcname = filename
            else:
                arcname = os.path.join(os.path.relpath(dirname, src),filename)
            logger.info('zipping {} as {}'.format(absname,arcname))
            zf.write(absname, arcname)
    zf.close()

if __name__ == "__main__":
    try:
        # logging
        logger = logging.getLogger('cbz')
        logger.setLevel(logging.DEBUG)
        # file handler
        fh = logging.FileHandler(os.path.expanduser('~/Library/Logs/cbz.log'))
        fh.setLevel(logging.DEBUG)
        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        # arguments management
        parser = argparse.ArgumentParser(description='CBZ utility')
        parser.add_argument('-t', '--tags', action='store_true', help='Preserve OSX tags (uses https://github.com/jdberry/tag)')
        parser.add_argument('-r', '--rename', action='store_true', help='Rename files using natural sort')
        parser.add_argument('-f', '--flatten', action='store_true', help='Flatten archive by removing folder structure')
        parser.add_argument('-d', '--destination', nargs=1,  help='Destination for processed files. If unspecified working directory is used instead')
        parser.add_argument('infiles', nargs='+')
        args = parser.parse_args()
        
        logger.debug('Args: {}'.format(args))
        
        # temporary items that will need cleanup
        tmp = []
        
        # destination folder
        if args.destination:
            dest = os.path.abspath(args.destination[0])
        else:
            dest = os.getcwd()
        if not os.path.exists(dest):
            os.makedirs(dest)
        logger.debug('Destination folder: {}'.format(dest))
        
        for f in args.infiles:    
            f = os.path.abspath(f)
            if os.path.isdir(f):
                logger.debug('Processing directory recursively: {}'.format(f))
                for dirname, folders, files in os.walk(f):
                    logger.debug('Processing directory: {}'.format(dirname))
                    # ignore hidden files
                    files = [f for f in files if not f[0] == '.']
                    if files:
                        target = '{}.cbz'.format(os.path.basename(os.path.normpath(dirname)))
                        target = os.path.join(dest,target)
                        zipFile(dirname,target,args.flatten,args.rename)   
            else:
                logger.debug('Processing file: {}'.format(f))
                
                if args.tags:
                    tags = getTags(f)
                    logger.debug('File {} has tags: {}'.format(f,tags))
                
                tmpdir = unpack(f)
                root, _ = os.path.splitext(os.path.basename(f))
                target = '{}.cbz'.format(root)
                target = os.path.join(dest,target)
                zipFile(tmpdir,target,args.flatten,args.rename)
                if args.tags:
                    logger.debug('Restore tags "{}" on file {}'.format(tags,target))
                    setTags(target, tags)
        cleanup()
    except Exception, e:
        logger.exception(e)
