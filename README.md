comics-utils
============

Scripts to manage my digital comics collection

cbz.py
------
CBZ utility can be used on both archives, to cleanup existing cbz/cbr/cb7, and folders, to create a new cbz archive.
Folders are processed recursively.
Options include:
 - preserving OSX tags (for archives only)
 - flatten the directory structure (same as -j option on zip)
 - rename files using natural sort

**Requires**
 * Python 2.7+
 * [jdberry/tag](https://github.com/jdberry/tag) (if using the --tags option)
 * [natsort](https://pypi.python.org/pypi/natsort)
 * [The Unarchiver command line tools](http://unarchiver.c3.cx/commandline)

**Usage**
```
usage: cbz.py [-h] [--tags] [--rename] [--flatten] [--destination DESTINATION]
              infiles [infiles ...]

CBZ utility

positional arguments:
  infiles

optional arguments:
  -h, --help            show this help message and exit
  --tags, -t            Preserve OSX tags (uses
                        https://github.com/jdberry/tag)
  --rename, -r          Rename files using natural sort
  --flatten, -f         Flatten archive by removing folder structure
  --destination DESTINATION, -d DESTINATION
                        Destination for processed files. If unspecified
                        working directory is used instead
```

sync-folder.py
--------------
Use OSX tags to create a replica of your directory structure for easy replication with [Cheetah Sync](http://www.jrtstudio.com/cheetah-sync-android-wireless-sync).
Folders have to be tagged 'sync' (works on parent folders as well).
Files tagged 'read' are ignored.

You have to edit the source to change the source and destination folders.

**Requires**
 * Python 2.7+
 * [jdberry/tag](https://github.com/jdberry/tag)

**Usage**
```
> python sync-folder.py
```