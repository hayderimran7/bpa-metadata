#!/bin/bash

PROJECT_NAME="bpa_downloads"
PROJECT_SOURCE="bpa-downloads-static"
TOPDIR=$(cd $(dirname $0); pwd)
SETUP_PATH="${TOPDIR}/${PROJECT_SOURCE}/tools/"
PIP_OPTS="-M --download-cache ~/.pip/cache --index-url=https://simple.crate.io"

VIRTUALENV="${HOME}/virt_${PROJECT_NAME}"
PYTHON="${VIRTUALENV}/bin/python"
PIP="${VIRTUALENV}/bin/pip"

######### Logging ##########
COLOR_NORMAL=$(tput sgr0)
COLOR_RED=$(tput setaf 1)
COLOR_YELLOW=$(tput setaf 3)
COLOR_GREEN=$(tput setaf 2)

set -e

log_error() {
    echo ${COLOR_RED}ERROR: $* ${COLOR_NORMAL}
}

log_warning() {
    echo ${COLOR_YELLOW}WARNING: $* ${COLOR_NORMAL}
}

log_success() {
    echo ${COLOR_GREEN}SUCCESS: $* ${COLOR_NORMAL}
}

log_info() {
    echo INFO: $*
}

# no news is good news
log() {
    ERROR_CODE=$0
    MESSAGE=$1

    if [ ${ERROR_CODE} != 0 ]
    then
        log_warning ${MESSAGE}
    else
        log_success ${MESSAGE}
    fi
}

is_root() {
   if [[ ${EUID} -ne 0 ]]
   then
       log_error "$0 needs to be run as root for this action."
       exit 1
   fi
}


linksource() {
	if [[ ! -d ~/bpa-metadata ]]
	then
		ln -s /usr/local/src/ ~/bpa-metadata
	fi
}

is_running_in_instance() {
    if [ ${USER} == 'ubuntu' ]
    then
       return 0
    else
       return 1
    fi
}

# make the virtualenv and install all the dependencies to build the linktree
# this includes the swift client
install_downloads_virtualenv() {
    log_info "Installing ${PROJECT_NAME}'s dependencies in virtualenv ${VIRTUALENV}"
    if is_running_in_instance
    then
        virtualenv ${VIRTUALENV}
        (
           source ${VIRTUALENV}/bin/activate
           cd ${SETUP_PATH}
           ${PIP} install ${PIP_OPTS} -e .[dev,tests,downloads]
           deactivate
        )

        mkdir -p ${HOME}/bin
        ln -sf ${VIRTUALENV}/bin/python ${HOME}/bin/vpython-${PROJECT_NAME}
        ln -sf ${VIRTUALENV}/bin/django-admin.py ${HOME}/bin/${PROJECT_NAME}
    else
        log_warning "Not running in a env where creating a virtualenv here would make sense"
        log_warning "shell into your instance and try again, or use the ccg remote command"
    fi
}

activate_virtualenv() {
    source ${VIRTUALENV}/bin/activate
}

deploy_webroot() {
    cp -r ${PROJECT_SOURCE/webroot/*} /var/www/
}

linksource
install_downloads_virtualenv
deploy_webroot

activate_virtualenv
${PROJECT_SOURCE}/tools/bpa-downloads-cron.sh





# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
