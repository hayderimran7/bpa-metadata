#!/bin/bash

# This script periodically checks the bpa archive for new files and re-build the BPA
# static downloads site allowing the new files to be downloaded via the static site.

WORKING_DIR=${HOME}
LINKBASE=${1:-"https://downloads.bioplatforms.com"}

# script run from cron to update the published link tree.
cd ~/bpa-metadata/bpa-downloads-static/tools || exit 1

# swift virtualenv
. ${WORKING_DIR}/virt_bpa_downloads/bin/activate

# swift credentials
. /etc/bpaswift/swift_creds.sh

tmpdir=${WORKING_DIR}/var/linktree/tmp/
apachedir=${WORKING_DIR}/var/linktree/apache/
mkdir -p "${tmpdir}"
mkdir -p "${apachedir}"

update_apache() {
    container="$1"   # the swift container name
    container_link="$2"  # the folder name used for the web front-end
    dummy=${WORKING_DIR}/var/linktree/"${container}"
    # make or update a dummy BPA archive
    mkdir -p "${dummy}"
    ./swift-dummy.sh "$container" "${dummy}"
    cfgtmp="$tmpdir/${container}.cfg"
    cfgprod="$apachedir/${container}.cfg"
    # generate link tree, and if successful update apache config
    mkdir -p /var/www/"${container_link}"/
    ./bpalink.py \
        --apacheredirects "${cfgtmp}" \
        --swiftbase http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea/"${container}" \
        --htmlbase /var/www/"${container_link}"/ \
        --linkbase ${LINKBASE} \
        "${container_link}" "${dummy}" && (
            test -e "${cfgtmp}" && mv "${cfgtmp}" "${cfgprod}"
        )
}

# any new entries here will need a matching include in /etc/apache2/sites-enabled/000-default
update_apache Melanoma melanoma
update_apache GBR gbr
update_apache Wheat7a wheat7a
update_apache BASE base
update_apache Wheat_Pathogens wheat_pathogens
update_apache Wheat_Cultivars wheat_cultivars

# requires this line in sudoers:
# ccg-user ALL=(ALL) NOPASSWD: /usr/sbin/apachectl
sudo apachectl graceful

