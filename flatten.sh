#!/bin/bash

for file in "$@"
do
    tmp=$(mktemp -dt tmp)
	unar -o $tmp "$file"
	tags=$(tag -lN "$file")
	
	#flatten structure
	find $tmp -type f -print0 | xargs -0 -I%%% mv %%% $tmp
	
	#rename files with human sort
	i=1
	files=$(find $tmp -type f -not -name ".*" | gsort -V)
	for f in $files; do
	  new=$(printf "%04d" ${i}) #04 pad to length of 4
	  ext=${f##*.}
	  mv ${f} $tmp/${new}.${ext}
	  let i=i+1
	done
	
	rm "$file"
	new="${file%.*}.cbz"
	zip -0rj "$new" ${tmp}/*
	tag -s $tags "$new"
	rm -fr $tmp
done
