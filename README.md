comics-utils
============

Scripts to manage my digital comics collection

makeCBZ.sh
----------
Use to create massively CBZ archives from folders containing image files.

**Usage**
```
pwd> /path/to/makeCBZ.sh
```

flatten.sh
----------
Extract archive content to temporary folder, and rezip using store level (-0) and remove junk folders (-j).

**Requires**
 * [The Unarchiver command line tools](http://unarchiver.c3.cx/commandline)

**Usage**
```
> /path/to/flatten.sh archive.cbz

> find . -name '*.cbz -print0 | xargs -0 /path/to/flatten.sh
```

sync-folder.py
--------------
Use OSX tags to create a replica of your directory structure for easy replication with [Cheetah Sync](http://www.jrtstudio.com/cheetah-sync-android-wireless-sync).
Folders have to be tagged 'sync' (works on parent folders as well).
Files tagged 'read' are ignored.

You have to edit the source to change the source and destination folders.

**Requires**
 * Python 2.7+
 * [tag](https://github.com/jdberry/tag)

**Usage**
```
> python sync-folder.py
```
