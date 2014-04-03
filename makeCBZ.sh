#!/bin/bash
pwd=`pwd`
find "$pwd" -type d -not -empty -print0 | while IFS= read -r -d '' dir; do
  if find "$dir" -maxdepth 1 -type f | read f; then
    zip -0j "$pwd"/"$(basename "$dir").cbz" "$dir"/*
  fi
done
