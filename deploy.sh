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


set_key_permissions() {
   if [ -f ${PROD_KEY_FILE} ]
   then
      chmod 600 ${PROD_KEY_FILE}
   else
      log_error "Production key missing. Install that and try again"
   fi
}

shell() {
   set_key_permissions
   ccg ${AWS_PROD_INSTANCE} shell
}


puppet() {
   set_key_permissions
   ccg ${AWS_PROD_INSTANCE} puppet
}

usage() {
    log_warning "Usage ./deploy.sh shell"
    log_warning "Usage ./deploy.sh puppet"
    log_warning "Usage ./deploy.sh nuclear"
}


nuclear() {
    log_info "Total rebuild of DB"
    bpam reset_db --router=default --traceback
    bpam syncdb --noinput --traceback
    bpam migrate --traceback
    bpam runscript set_initial_bpa_projects --traceback
    bpam runscript ingest_users
    bpam runscript ingest_gbr
    bpam runscript ingest_melanoma
    # wheat
    bpam runscript ingest_wheat_pathogens
    bpam runscript ingest_wheat_cultivars
    # base
    bpam runscript ingest_landuse
    bpam runscript ingest_base_454
    bpam runscript ingest_base_contextual
    bpam runscript ingest_base_metagenomics
    # links
    bpam runscript url_checker
}

case ${ACTION} in
    shell)
        shell
        ;;
    puppet)
        puppet
        ;;
    nuclear)
        nuclear
        ;;
    *)
        usage
esac
