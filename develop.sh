#!/bin/bash
# Script to control bpam in dev and test

TOPDIR=$(cd $(dirname $0); pwd)

ACTION=$1

PROJECT_NAME='bpam'
VIRTUALENV="${HOME}/virt_${PROJECT_NAME}"
AWS_STAGING_INSTANCE='ccg_syd_nginx_staging'


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

activate_virtualenv() {
   if [ ! -d ${VIRTUALENV} ]
   then
        log_warning "There is no ${VIRTUALENV} here, making it."
        virtualenv ${VIRTUALENV}
        . ${VIRTUALENV}/bin/activate
        pip install fig
        pip install 'flake8>=2.0,<2.1'
   else
      source ${VIRTUALENV}/bin/activate
   fi
}


is_root() {
   if [[ ${EUID} -ne 0 ]]
   then
       log_error "$0 needs to be run as root for this action."
       exit 1
   fi
}


# ssh setup, make sure our ccg commands can run in an automated environment
ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging-2014.pem
}


pythonlint() {
    activate_virtualenv
    ${VIRTUALENV}/bin/flake8 ${PROJECT_NAME} --exclude=migrations --ignore=E501 --count
}


unit_tests() {
    activate_virtualenv

    mkdir -p data/tests
    chmod o+rwx data/tests
    fig --project-name bpam -f fig-test.yml up
}

up() {
    activate_virtualenv
    mkdir -p data/dev
    chmod o+rwx data/dev

    fig --project-name bpa-metadata up
}


selenium() {
    activate_virtualenv
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    fig --project-name bpa-metadata -f fig-selenium.yml up
}


ci_staging() {
    ccg ${AWS_STAGING_INSTANCE} drun:'mkdir -p bpam/docker/unstable'
    ccg ${AWS_STAGING_INSTANCE} drun:'mkdir -p bpam/data'
    ccg ${AWS_STAGING_INSTANCE} drun:'chmod o+w bpam/data'
    ccg ${AWS_STAGING_INSTANCE} putfile:fig-staging.yml,bpam/fig-staging.yml
    ccg ${AWS_STAGING_INSTANCE} putfile:docker/unstable/Dockerfile,bpam/docker/unstable/Dockerfile

    ccg ${AWS_STAGING_INSTANCE} drun:'cd bpam && fig -f fig-staging.yml stop'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd bpam && fig -f fig-staging.yml kill'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd bpam && fig -f fig-staging.yml rm --force -v'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd bpam && fig -f fig-staging.yml build --no-cache webstaging'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd bpam && fig -f fig-staging.yml up -d'
    ccg ${AWS_STAGING_INSTANCE} drun:'docker-untagged || true'
}

rpmbuild() {
    activate_virtualenv
    mkdir -p data/rpmbuild
    chmod o+rwx data/rpmbuild

    fig --project-name bpam -f fig-rpmbuild.yml up
}


rpm_publish() {
    time ccg publish_testing_rpm:data/rpmbuild/RPMS/x86_64/bpam*.rpm,release=6
}

usage() {
    log_warning "Usage ./develop.sh (pythonlint|jslint)"
    log_warning "Usage ./develop.sh (unit_tests)"
    log_warning "Usage ./develop.sh (selenium)"
    log_warning "Usage ./develop.sh (rpmbuild|rpm_publish|ci_staging)"
    log_warning "Usage ./develop.sh (start|up)"
    log_warning "Usage ./develop.sh (usage)"
}


case ${ACTION} in
pythonlint)
    pythonlint
    ;;
jslint)
    jslint
    ;;
rpmbuild)
    rpmbuild
    ;;
rpm_publish)
    ci_ssh_agent
    rpm_publish
    ;;
ci_staging)
    ci_ssh_agent
    ci_staging
    ;;
start)
    up
    ;;
up)
    up
    ;;
unit_tests)
    unit_tests
    ;;
selenium)
    selenium
    ;;
*)
    usage
esac
