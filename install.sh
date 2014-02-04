#!/bin/bash

TARGET="/home/ubuntu/"

DOWNLOADS_REPO="ssh://hg@bitbucket.org/ccgmurdoch/bpa-downloads-web-site"
DOWNLOADS_DEST="${TARGET}/bpa-downloads-web-site"

METADATA_REPO="ssh://hg@bitbucket.org/ccgmurdoch/bpa-metadata"
METADATA_DEST="${TARGET}/bpa-metadata"

hg clone ${DOWNLOADS_REPO} ${DOWNLOADS_DEST}
hg clone ${METADATA_REPO} ${METADATA_DEST}

