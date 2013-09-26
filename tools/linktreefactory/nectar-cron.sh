#!/bin/bash

# script run from cron on cortex to update the published 
# link tree.
cd ~/bpa-metadata/tools/linktreefactory || exit 1

# swift virtualenv
 . ~/swiftev/bin/activate

# swift credentials
. ./swift-creds.sh

tmpdir=~/var/linktree/tmp/
apachedir=~/var/linktree/apache/
mkdir -p "$tmpdir"
mkdir -p "$apachedir"

update_apache() {
    container="$1"
    linkmethod="$2"
    dummy=~/var/linktree/"$container"
    # make or update a dummy BPA archive
    mkdir -p "$dummy"
    ./swift-dummy.sh "$container" "$dummy"
    cfgtmp="$tmpdir/$container.cfg"
    cfgprod="$apachedir/$container.cfg"
    # generate link tree, and if successful update apache config
    mkdir -p /var/www/test/"$linkmethod"/
    ./bpalink2.py \
        -a "$cfgtmp" \
        -s http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea/"$container" \
        -h /var/www/test/"$linkmethod"/index.html \
        -b https://downloads.bioplatforms.com/ \
        "$linkmethod" "$dummy" && (
            mv "$cfgtmp" "$cfgprod"
        )
}

# any new entries here will need a matching include in /etc/apache2/sites-enabled/000-default
update_apache Melanoma melanoma
update_apache GBR gbr

# requires this line in sudoers:
# ccg-user ALL=(ALL) NOPASSWD: /usr/sbin/apachectl
sudo apachectl graceful

