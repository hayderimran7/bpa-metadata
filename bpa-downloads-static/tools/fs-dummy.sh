#!/bin/bash

cd "$1" || exit 0
find . -mindepth 1 -type d -exec mkdir "$2"/{} \;
find . -type f -exec touch "$2"/{} \;
find . -type f -size -1000k -exec cp -a {} "$2"/{} \;

