#!/bin/bash

WORKING_DIR="/home/ubuntu/"

# script run from cron to update the published link tree.
cd ~/bpa-metadata/bpa-downloads-static/tools || exit 1

# swift virtualenv
. ${WORKING_DIR}/virt_bpa_downloads/bin/activate

# swift credentials
. /etc/bpaswift/swift_creds.sh

tmpdir=${WORKING_DIR}/var/linktree/tmp/
apachedir=${WORKING_DIR}/var/linktree/apache/
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
    mkdir -p /var/www/"$linkmethod"/
    ./bpalink.py \
        --apacheredirects "$cfgtmp" \
        --swiftbase http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea/"$container" \
        --htmlbase /var/www/"$linkmethod"/ \
        --linkbase https://downloads.bioplatforms.com/ \
        "$linkmethod" "$dummy" && (
            test -e "$cfgtmp" && mv "$cfgtmp" "$cfgprod"
        )
}

# any new entries here will need a matching include in /etc/apache2/sites-enabled/000-default
#update_apache Melanoma melanoma
#update_apache GBR gbr
#update_apache Wheat7a wheat7a
#update_apache BASE base
#update_apache Wheat_Pathogens wheat_pathogens
update_apache Wheat_Cultivars wheat_cultivars

# requires this line in sudoers:
# ccg-user ALL=(ALL) NOPASSWD: /usr/sbin/apachectl
sudo apachectl graceful

