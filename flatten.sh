#!/bin/bash

for file in "$@"
do
    tmp=$(mktemp -dt tmp)
	unar -o $tmp "$file"
	rm "$file"
	zip -0rj "$file" ${tmp}/*
	rm -fr $tmp
done
