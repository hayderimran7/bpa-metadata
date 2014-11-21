#!/bin/bash
# Script to control bpam in dev and test

TOPDIR=$(cd $(dirname $0); pwd)
ACTION=$1
SECOND_ARGUMENT=$2
shift

PORT='8000'

PROJECT_NAME='bpam'
AWS_BUILD_INSTANCE='aws_rpmbuild_centos6'
AWS_STAGING_INSTANCE='aws-syd-bpam-staging'
TARGET_DIR="/usr/local/src/${PROJECT_NAME}"
CONFIG_DIR="${TOPDIR}/${PROJECT_NAME}"
PIP_OPTS="-v --download-cache ~/.pip/cache --index-url=https://pypi.python.org/simple"
PIP5_OPTS="${PIP_OPTS} --process-dependency-links --allow-all-external"
PYVENV="virtualenv-2.7"
VIRTUALENV="${TOPDIR}/virt_${PROJECT_NAME}"
PYTHON="${VIRTUALENV}/bin/python"
PIP="${VIRTUALENV}/bin/pip"
DJANGO_ADMIN="${VIRTUALENV}/bin/django-admin.py"

# tests need extra python modules
TESTING_MODULES="PyVirtualDisplay selenium nose sure>=1.2.1 Werkzeug"
CI_MODULES="coverage==3.6"

export PATH=/usr/pgsql-9.3/bin:${PATH}

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
        log_error "There is no ${VIRTUALENV} here, activate virtualenv failed."
        exit 1
    fi
    source ${VIRTUALENV}/bin/activate
}


is_root() {
   if [[ ${EUID} -ne 0 ]]
   then
       log_error "$0 needs to be run as root for this action."
       exit 1
   fi
}

settings() {
    export DEBUG_TOOLBAR=True
    export DJANGO_SETTINGS_MODULE="${PROJECT_NAME}.settings"
}

# ssh setup, make sure our ccg commands can run in an automated environment
ci_ssh_agent() {
    ssh-agent > /tmp/agent.env.sh
    source /tmp/agent.env.sh
    ssh-add ~/.ssh/ccg-syd-staging.pem
}

build_number_head() {
    export TZ=Australia/Perth
    DATE=$(date)
    TIP=$(hg tip --template {node} 2>/dev/null || /bin/true)
    log_info "Generated by develop.sh"
    log_info "build.timestamp=${DATE}"
    log_info "build.tip=${TIP}"
}


make_local_rpm() {
    CCGSOURCEDIR=/usr/local/src rpmbuild -bb centos/bpam.spec
}

# build RPMs on a remote host from ci environment
ci_remote_build() {
    log_info "Building rpm on ${AWS_BUILD_INSTANCE}"
    time ccg ${AWS_BUILD_INSTANCE} boot
    time ccg ${AWS_BUILD_INSTANCE} puppet
    time ccg ${AWS_BUILD_INSTANCE} shutdown:50

    cd ${TOPDIR}

    if [ -z "$BAMBOO_BUILDKEY" ]; then
        log_info "We aren't running under Bamboo, create new build-number.txt."
        build_number_head > build-number.txt
    else
        log_info "Bamboo has already put some useful information in build-number.txt, so append to it."
        build_number_head >> build-number.txt
    fi

    EXCLUDES="('bootstrap'\, '.hg*'\, '.git'\, 'virt*'\, '*.log'\, '*.rpm'\, 'bpam/build'\, 'bpam/dist'\, '*.egg-info')"
    SSH_OPTS="-o StrictHostKeyChecking\=no"
    RSYNC_OPTS="-l"
    time ccg ${AWS_BUILD_INSTANCE} rsync_project:local_dir=./,remote_dir=${TARGET_DIR}/,ssh_opts="${SSH_OPTS}",extra_opts="${RSYNC_OPTS}",exclude="${EXCLUDES}",delete=True
    time ccg ${AWS_BUILD_INSTANCE} build_rpm:centos/${PROJECT_NAME}.spec,src=${TARGET_DIR}
}

ci_fetch_rpm() {
    mkdir -p build
    log_info "Fetching rpm from ${AWS_BUILD_INSTANCE}"
    ccg ${AWS_BUILD_INSTANCE} getfile:rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,build/
}


# publish rpms
ci_rpm_publish() {
    log_info "Publishing rpm to testing"
    time ccg publish_testing_rpm:build/${PROJECT_NAME}*.rpm,release=6
}


# destroy our ci build server
ci_remote_destroy() {
    ccg ${AWS_BUILD_INSTANCE} destroy
}


# puppet up staging which will install the latest rpm
ci_staging() {
    ccg ${AWS_STAGING_INSTANCE} boot
    ccg ${AWS_STAGING_INSTANCE} puppet
}

ci_staging_lettuce() {
    ccg ${AWS_STAGING_INSTANCE} dsudo:'dbus-uuidgen --ensure'
    ccg ${AWS_STAGING_INSTANCE} dsudo:'chown apache:apache /var/www'
    ccg ${AWS_STAGING_INSTANCE} dsudo:'service httpd restart'
    ccg ${AWS_STAGING_INSTANCE} dsudo:'bpam run_lettuce --with-xunit --xunit-file\=/tmp/tests.xml || true'
    ccg ${AWS_STAGING_INSTANCE} getfile:/tmp/tests.xml,./
}

# lint using flake8
lint() {
    activate_virtualenv
    cd ${TOPDIR}
    flake8 ${PROJECT_NAME} --ignore=E501 --count
}

is_running_in_instance() {
    if [ ${USER} == 'ccg-user' ]
    then
       return 0
    else
       return 1
    fi
}

install() {
    log_info "Installing ${PROJECT_NAME}'s dependencies in virtualenv ${VIRTUALENV}"
    if is_running_in_instance
    then
        ${PYVENV} --system-site-packages ${VIRTUALENV}
        (
           source ${VIRTUALENV}/bin/activate
           cd ${CONFIG_DIR}
           pip install ${PIP_OPTS} --force-reinstall --upgrade 'pip>=1.5,<1.6'
           pip install ${PIP5_OPTS} -e .[dev,tests,downloads]
           pip install ${PIP5_OPTS} ${CI_MODULES} ${TESTING_MODULES}
           deactivate
        )

        mkdir -p ${HOME}/bin
        ln -sf ${VIRTUALENV}/bin/python ${HOME}/bin/vpython-${PROJECT_NAME}
        ln -sf ${VIRTUALENV}/bin/django-admin.py ${HOME}/bin/${PROJECT_NAME}
    else
        log_warning "Not running in a env where creating a virtualenv here would make sense, the virtualenv python needs to link to the lxc python."
        log_warning "shell into your instance and try again, or use the ccg remote command."
    fi
}

########################################
# local lxc related

make_local_instance() {
    if ! is_running_in_instance
    then
       log_info "Making a local build instance"
       rm -rf virt_${PROJECT_NAME}
       ccg --nuke-bootstrap
       ccg dev puppet
    else
       log_warning "Seems like I'm running in a build instance of some sorts already. Aborting."
    fi
}

runingest() {
    activate_virtualenv
    CMD='python ./bpam/manage.py'
    ${CMD} runscript --traceback ${SECOND_ARGUMENT}
}

ingest_all() {
    activate_virtualenv
    CMD='python ./bpam/manage.py'
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
}

devrun() {
    ${DJANGO_ADMIN} syncdb --traceback --noinput
    ${DJANGO_ADMIN} migrate --traceback
    ingest_all
    startserver
}

# django syncdb, migrate and collect static
syncmigrate() {
    activate_virtualenv
    log_info "Running syncdb"
    ${DJANGO_ADMIN} syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> syncdb-develop.log
    log_info "Running migrate"
    ${DJANGO_ADMIN} migrate --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> migrate-develop.log
    log_info "Running collectstatic"
    ${DJANGO_ADMIN} collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> collectstatic-develop.log

    ingest_all
}


ipaddress() {
    if [ -n "$1" ]; then
        DEV="dev $1"
    else
        DEV=""
    fi
    ip -4 addr show ${DEV} 2> /dev/null | awk '/inet / { gsub(/\/.*/, ""); print $2; }'
}

# start runserver
startserver() {
    settings
    echo "Visit http://$(ipaddress eth0):${PORT}/"
    # ${VIRTUALENV}/bin/django-admin.py runserver_plus 0.0.0.0:${PORT} --traceback
    ${VIRTUALENV}/bin/python bpam/manage.py runserver_plus 0.0.0.0:${PORT} --traceback
}

pythonversion() {
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/python -V
}

pipfreeze() {
    log_info "${PROJECT_NAME} pip freeze"
    ${TOPDIR}/virt_${PROJECT_NAME}/bin/pip freeze
}

clean() {
    log_info "Cleaning"
    find ${TOPDIR}/${PROJECT_NAME} -name "*.pyc" -exec rm -rf {} \;
}

purge() {
    log_info "Purging"
    rm -rf ${TOPDIR}/virt_${PROJECT_NAME}
    rm *.log
}


dev() { 
    activate_virtualenv
    devrun
}

coverage() {
    activate_virtualenv
    log_info "Running coverage with reports"
    coverage `run ../manage.py test --settings=bpam.nsettings.test --traceback`
    coverage html --include=" $ SITE_URL*" --omit="admin.py"
}

unittest() {
    log_info "Running Unit Test"
    activate_virtualenv
    (
       cd ${CONFIG_DIR}
       python manage.py test --settings=bpam.nsettings.test --traceback
    )
}

url_checker() {
    activate_virtualenv
    ${DJANGO_ADMIN} runscript url_checker --traceback
}


deepclean() {
    activate_virtualenv	
    CMD='python ./bpam/manage.py'
    ${CMD} reset_db --user=postgres --router=default --traceback
    log_info "Deepclean syncing"
    ${CMD} syncdb --noinput --traceback
    log_info "Deepclean Migrating"
    ${CMD} migrate --traceback
}

nuclear() {
    deepclean
    ingest_all
}

usage() {
    log_warning "Usage ./develop.sh make_local_instance"
    log_warning "Usage ./develop.sh load_base"
    log_warning "Usage ./develop.sh (lint|jslint)"
    log_warning "Usage ./develop.sh (unittest|coverage)"
    log_warning "Usage ./develop.sh (start|install|clean|purge|pipfreeze|pythonversion)"
    log_warning "Usage ./develop.sh (ci_remote_build|ci_remote_build_and_fetch|ci_staging|ci_rpm_publish|ci_remote_destroy)"
    log_warning "Usage ./develop.sh (nuclear)"
    log_warning "Usage ./develop.sh (wheat_pathogens_dev)"
    log_warning "Usage ./develop.sh url_checker"
    log_warning "Usage ./develop.sh deepclean"
    log_warning "Usage ./develop.sh migrationupdate APP"
    log_warning "Usage ./develop.sh runingest ingest_script"
}

load_base() {
    activate_virtualenv
    CMD='python ./bpam/manage.py'
    deepclean
    ${CMD} runscript set_initial_bpa_projects --traceback
    ${CMD} runscript ingest_users --traceback
    ${CMD} runscript ingest_base_454 --traceback
    ${CMD} runscript ingest_base_metagenomics --traceback
}

migrationupdate() {
    settings
    APP=${SECOND_ARGUMENT}
    ${DJANGO_ADMIN} schemamigration ${APP} --auto --update
    ${DJANGO_ADMIN} migrate ${APP}
}

case ${ACTION} in
    migrationupdate)
        migrationupdate
        ;;
    deepclean)
        deepclean
        ;;
    coverage)
        coverage
        ;;
    unittest)
        unittest
        ;;
    nuclear)
        nuclear
        ;;
    pythonversion)
        pythonversion
        ;;
    pipfreeze)
        pipfreeze
        ;;
    lint)
        lint
        ;;
    syncmigrate)
        syncmigrate
        ;;
    start)
        startserver
        ;;
    install)
        install
        ;;
    ci_remote_build)
        ci_ssh_agent
        ci_remote_build
        ;;
    ci_remote_destroy)
        ci_ssh_agent
        ci_remote_destroy
        ;;
    ci_rpm_publish)
        ci_ssh_agent
        ci_rpm_publish
        ;;
    ci_staging)
        ci_ssh_agent
        ci_staging
        ;;
    ci_staging_tests)
        ci_ssh_agent
        ci_staging_lettuce
        ;;
    ci_fetch_rpm)
        ci_fetch_rpm
        ;;
    ci_remote_build_and_fetch)
        ci_ssh_agent
        ci_remote_build
        ci_fetch_rpm
        ;;
    clean)
        clean
        ;;
    purge)
        clean
        purge
        ;;
    dev)
        dev
        ;;
    make_local_instance)
        make_local_instance
        ;;
    url_checker)
        url_checker
        ;;
    load_base)
        load_base
        ;;
    runingest)
        runingest
        ;;
    *)
        usage
esac
