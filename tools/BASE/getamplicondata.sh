#! /bin/bash

AMPLICON_CONTAINERS="BASE_Amplicon_16S BASE_Amplicon_18S BASE_Amplicon_ITS"
TARGET=${HOME}/var/amplicon_metadata/

get_metadata() {
    for c in ${AMPLICON_CONTAINERS}
    do
        for f in $(swift list $c | grep xlsx)
        do
        swift download $c $f
        done
    done
}

get_md5_lists() {
    for c in ${AMPLICON_CONTAINERS}
    do
        for f in $(swift list $c | grep md5)
        do
        swift download $c $f
        done
    done
}

mkdir -p ${TARGET}
(
   cd ${TARGET}
   get_metadata
   get_md5_lists
)

