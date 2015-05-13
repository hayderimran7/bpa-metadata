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
    # find . -type d -name ".ropeproject" -exec rm -fr {} \;
    ${VIRTUALENV}/bin/flake8 bpam --exclude=migrations,.ropeproject --ignore=E501,E303 --count
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


build() {
   activate_virtualenv
   fig --project-name ${PROJECT_NAME} build
}

rm_containers() {
   fig --project-name ${PROJECT_NAME} rm
}

entrypoint() {
   ENTRYPOINT=${1:-bash}
   log_info "Entrypoint ${ENTRYPOINT}"
   # docker run --rm -i -t -v $(pwd):/app/ --link="${PROJECT_NAME}_db_1:db" ${PROJECT_NAME}_web ${ENTRYPOINT} $2
   docker exec -it ${PROJECT_NAME}_web_1 ${ENTRYPOINT} $2
}

usage() {
   echo 'Usage ./develop.sh (build|shell|unit_tests|selenium|superuser|up|rm|ingest|ingest_all)'
   echo '                   build        Build all images'
   echo '                   shell        Create and shell into a new web image, used for db checking with Django env available'
   echo '                   superuser    Create Django superuser'
   echo '                   ingest       Ingest metadata'
   echo '                   ingest_all   Ingest metadata'
   echo '                   checksecure  Run security check'
   echo '                   up           Spins up docker image stack'
   echo '                   rm           Remove all containers'
   echo '                   ci_staging   Continuous Integration staging'
   echo '                   pythonlint   Run python lint'
   echo '                   unit_tests   Run unit tests'
   echo '                   selenium     Run selenium tests'
   echo '                   usage'
}

case ${ACTION} in
pythonlint)
    pythonlint
    ;;
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
rm)
    rm_containers
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
ingest_all)
    entrypoint ingest_all
    ;;
runscript)
    entrypoint runscript $2
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
checksecure)
    entrypoint checksecure
    ;;
*)
    usage
esac
