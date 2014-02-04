#!/bin/bash


clone_repo() {
    # this should only happen in production
    TARGET="/home/ubuntu/"

    METADATA_REPO="ssh://hg@bitbucket.org/ccgmurdoch/bpa-metadata"
    METADATA_DEST="${TARGET}/bpa-metadata"

    hg clone ${DOWNLOADS_REPO} ${DOWNLOADS_DEST}
}

if [[ ! -d ~/bpa-metadata ]]
then
    ln -s /usr/local/src/ ~/bpa-metadata
fi

