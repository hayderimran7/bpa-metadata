#!/bin/bash
# 

TOPDIR=$(cd $(dirname $0); pwd)
ACTION=$1
shift

PROJECT_NAME='bpa-metadata'
PROJECT_NICKNAME='bpam'

CMD="bpam"

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


usage() {
    log_warning "Usage deploy.sh ingest"
    log_warning "Usage deploy.sh nuclear"
}


nuclear() {
    ${CMD} reset_db --router=default --traceback
}

ingest() {
    ${CMD} syncdb --traceback --noinput
    ${CMD} migrate --traceback

    log_info "Ingest BPA Projects"
    ${CMD} runscript ingest_bpa_projects --traceback
    log_info "Ingest BPA Users"
    ${CMD} runscript ingest_users --traceback
    ${CMD} runscript ingest_melanoma --traceback
    ${CMD} runscript ingest_gbr --traceback
    ${CMD} runscript ingest_wheat_pathogens --traceback
    ${CMD} runscript ingest_wheat_pathogens_transcript --traceback
    ${CMD} runscript ingest_wheat_cultivars --traceback

    # BASE
    ${CMD} runscript ingest_base_454
    ${CMD} runscript ingest_base_metagenomics --traceback
    ${CMD} runscript ingest_base_landuse --traceback
    ${CMD} runscript ingest_base_contextual --traceback
    ${CMD} runscript ingest_base_amplicon --traceback
    ${CMD} runscript ingest_base_otu --traceback

    # links
    bpam runscript url_checker
}

case ${ACTION} in
    ingest)
        ingest
        ;;
    nuclear)
        nuclear
        ;;
    *)
        usage
esac
