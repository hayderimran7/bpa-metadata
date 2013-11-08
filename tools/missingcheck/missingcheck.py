#!/usr/bin/env python
# coding: utf-8

import fileinput


with open('./missing.txt') as missing_file:
    missing_files = [line.rstrip() for line in missing_file if line.strip() != '']

swift_files = []
for line in fileinput.input():
    swift_file = line.strip().split('/')[-1]
    if swift_file.find('.fastq'):
        swift_files.append(swift_file)

for missing in missing_files:
    if missing in swift_files:
        print('{0} is in swift'.format(missing))
