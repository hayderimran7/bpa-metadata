#!/bin/bash
# Script to control ${PROJECT_NAME} in dev and test

TOPDIR=$(cd $(dirname $0); pwd)

ACTION=$1

PROJECT_NAME='bpametadata'
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
    fig --project-name ${PROJECT_NAME} -f fig-test.yml up
}

up() {
    activate_virtualenv
    mkdir -p data/dev
    chmod o+rwx data/dev

    fig --project-name ${PROJECT_NAME} up
}


selenium() {
    activate_virtualenv
    mkdir -p data/selenium
    chmod o+rwx data/selenium

    fig --project-name ${PROJECT_NAME} -f fig-selenium.yml up
}


ci_staging() {
    ccg ${AWS_STAGING_INSTANCE} drun:'mkdir -p ${PROJECT_NAME}/docker/unstable'
    ccg ${AWS_STAGING_INSTANCE} drun:'mkdir -p ${PROJECT_NAME}/data'
    ccg ${AWS_STAGING_INSTANCE} drun:'chmod o+w ${PROJECT_NAME}/data'
    ccg ${AWS_STAGING_INSTANCE} putfile:fig-staging.yml,${PROJECT_NAME}/fig-staging.yml
    ccg ${AWS_STAGING_INSTANCE} putfile:docker/unstable/Dockerfile,${PROJECT_NAME}/docker/unstable/Dockerfile

    ccg ${AWS_STAGING_INSTANCE} drun:'cd ${PROJECT_NAME} && fig -f fig-staging.yml stop'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd ${PROJECT_NAME} && fig -f fig-staging.yml kill'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd ${PROJECT_NAME} && fig -f fig-staging.yml rm --force -v'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd ${PROJECT_NAME} && fig -f fig-staging.yml build --no-cache webstaging'
    ccg ${AWS_STAGING_INSTANCE} drun:'cd ${PROJECT_NAME} && fig -f fig-staging.yml up -d'
    ccg ${AWS_STAGING_INSTANCE} drun:'docker-untagged || true'
}

rpm_build() {
    activate_virtualenv
    mkdir -p data/rpmbuild
    chmod o+rwx data/rpmbuild

    fig --project-name ${PROJECT_NAME} -f fig-rpmbuild.yml up
}

rpm_publish() {
    time ccg publish_testing_rpm:data/rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,release=6
}

build() {
   activate_virtualenv
   fig --project-name ${PROJECT_NAME} build
}

clean() {
   fig --project-name ${PROJECT_NAME} rm
}

entrypoint() {
   ENTRYPOINT=${1:-bash}
   log_info "Entrypoint ${ENTRYPOINT}"
   docker run --rm -i -t -v $(pwd):/app/ --link="${PROJECT_NAME}_db_1:db" ${PROJECT_NAME}_web ${ENTRYPOINT}
}

usage() {
   echo 'Usage ./develop.sh (build|shell|unit_tests|selenium|superuser|up|rm|rpm_build|rmp_publish|ingest)'
   echo '                   build        Build all images'
   echo '                   shell        Create and shell into a new web image, used for db checking with Django env available'
   echo '                   superuser    Create Django superuser'
   echo '                   ingest       Ingest metadata'
   echo '                   up           Spins up docker image stack'
   echo '                   rm           Remove all images'
   echo '                   rpm_build    Build rpm'
   echo '                   rpm_publish  Publish rpm'
   echo '                   ci_staging   Continuous Integration staging'
   echo '                   rpm_publish  Publish rpm'
   echo '                   pythonlint   Run python lint'
   echo '                   jslint       Run javascript lint'
   echo '                   unit_tests   Run unit tests'
   echo '                   selenium     Run selenium tests'
   echo '                   usage'
}

case ${ACTION} in
pythonlint)
    pythonlint
    ;;
jslint)
    jslint
    ;;
rpm_build)
    rpm_build
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
build)
    build
    ;;
clean)
    clean
    ;;
up)
    up
    ;;
shell)
    entrypoint
    ;;
superuser)
    entrypoint superuser
    ;;
ingest)
    entrypoint ingest
    ;;
nuclear)
    entrypoint nuclear
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
