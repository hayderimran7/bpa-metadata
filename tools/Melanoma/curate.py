#! /usr/bin/env python
# -*- coding: utf-8 -*-  

import csv
import os
import time 
import sys

#TARGET="/media/bigdisk/melanoma_target"
TARGET="./melanoma_target"

def strip(st):
    st = st.decode('utf8', 'ignore')
    return st.strip().strip(u'\u200B\ufeff')

def get_disk_files():
    allfiles = {}
    for root, folder, files in os.walk("/media/bigdisk/raw/"):
        for f in files:
            if f.endswith(('.gz',)):
                fullpath = os.path.join(root, f)
                if f in allfiles:
                    allfiles[f].append(fullpath)
                else:
                    allfiles[f] = [fullpath]

    return allfiles
    
def get_csv_data(source_file):
    csv_data = {}
    with open(source_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = strip(row["Sequence file names - supplied by sequencing facility"])
            if name == "":
                continue

            # some files have folder prefixes, get rid of those
            if name.find('/') != -1:
                name = name.split('/')[-1]

            bpa_id = strip(row["Unique Identifier"])
            if bpa_id is "":
                continue
            if bpa_id.find("/") == -1:
                continue 

            xid = bpa_id.split("/")[1]

            if xid in csv_data:
                csv_data[xid].append(name)
            else:
                csv_data[xid] = [name]

    return csv_data
            

def process_csv(disk_files, csv_data):
    """
    Find file mentioned in csv file and link it into target folder
    if there were duplicates link them too, but prefix with DUP_n
    """
    for xid, names in csv_data.items():
        xid_path = os.path.join(TARGET, xid)
        if not os.path.exists(xid_path):
            os.makedirs(xid_path)
            
        for name in names:
            if name in disk_files:
                # there may be duplicates
                for i, _f in enumerate(disk_files[name]):
                    if i == 0:
                        tgt = os.path.join(xid_path, name)
                    else:
                        tgt = os.path.join(xid_path, "DUP{0}_{1}".format(str(i), name))

                    try:
                        os.symlink(_f, tgt)
                    except OSError, e:
                        print("When trying to {0} -> {1}, the followng happened:".format(_f, tgt))
                        print e
                        print("Ain't that a bitch.")



            else:
                print("[{0}] mentioned in csv file not on disk".format(name))


def main():
    csv_data = get_csv_data('./melanoma_study.csv')
    csv_pilot_data = get_csv_data('./pilot_data.csv')
    disk_files = get_disk_files()
   
    print("Propper Data") 
    process_csv(disk_files, csv_data)    

    print("Pilot Data") 
    process_csv(disk_files, csv_pilot_data)    


if __name__ == "__main__":
    main()
