#!/bin/bash

#
# creates a dummy BPA archive from the swift cluster, 
# consisting of all files < 1MB in size, and an empty 
# placeholder file for other files.
#
# to be used in conjunction with the bpalink2.py script.
#


bucket="$1"
target="$2"

usage() {
    echo "usage: $0 <bucket> <target>"
    exit 1
}

if [ x"$bucket" = x ]; then 
    usage
fi
if [ x"$target" = x ]; then 
    usage
fi

mkdir -p "$target"
cd "$target" || exit 1
# swift can sometimes download empty directories as files; so clear out anything that might be a directory (no dot in name)
find . -type f -regextype posix-extended -regex "^.*/[A-Z0-9a-z]+$" -and -size 0 -print -exec rm {} \;

( swift list "$bucket" ) | (
    while read F; do 
        if [ -f "$F" ]; then 
            #echo "already exists, skipping: $F"
            continue
        fi
        sz=`swift stat "$bucket" "$F" | grep 'Content Length'  | awk -F': ' {'print $2'}`
        if [ $sz -lt 1048576 ]; then 
            echo "swift download: $F"
            swift download "$bucket" "$F"
        else
            echo "making dummy: $F"
            mkdir -p "`dirname "$F"`"
            touch "$F"
        fi
    done
)

