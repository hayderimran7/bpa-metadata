#!/bin/bash

TOPDIR=$(cd $(dirname $0); pwd)
ACTION=$1
shift

PROJECT_NAME='bpa-metadata'
PROJECT_NICKNAME='bpam'
AWS_PROD_INSTANCE='aws-syd-bpa-metadata-prod'

PROD_KEY_FILE="${HOME}/.ssh/ccg-syd-ops.pem"

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


shell() {
   if [ -f ${PROD_KEY_FILE} ]
   then
      chmod 600 ${PROD_KEY_FILE}
   else
      log_error "Production key missing. Install that and try again"
   fi
   ccg ${AWS_PROD_INSTANCE} shell
}

usage() {
    log_warning "Usage ./deploy.sh shell"
}

case ${ACTION} in
    shell)
        shell
        ;;
    *)
        usage
esac
