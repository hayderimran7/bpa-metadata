#!/bin/bash
# Script to control bpa-metadata in dev and test

set -e

TOPDIR=$(cd $(dirname $0); pwd)
ACTION=$1
shift

PORT='8000'

PROJECT_NAME='bpa-metadata'
PROJECT_NICKNAME='bpam'
AWS_BUILD_INSTANCE='aws_rpmbuild_centos6'
AWS_STAGING_INSTANCE='aws-syd-bpa-metadata-staging'
TARGET_DIR="/usr/local/src/${PROJECT_NICKNAME}"
PIP_OPTS="-M --download-cache ~/.pip/cache --index-url=https://restricted.crate.io"

######### Logging ########## 
COLOR_NORMAL=$(tput sgr0)
COLOR_RED=$(tput setaf 1)
COLOR_YELLOW=$(tput setaf 3)
COLOR_GREEN=$(tput setaf 2)


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



devsettings() {
    export DJANGO_SETTINGS_MODULE="bpam.nsettings.dev"
}

activate_virtualenv() {
    source ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/activate
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

# build RPMs on a remote host from ci environment
ci_remote_build() {
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

    mkdir -p build
    ccg ${AWS_BUILD_INSTANCE} getfile:rpmbuild/RPMS/x86_64/${PROJECT_NAME}*.rpm,build/
}


# publish rpms
ci_rpm_publish() {
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
    ccg ${AWS_STAGING_INSTANCE} shutdown:50
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

# lint js, assumes closure compiler
jslint() {
    JSFILES="${TOPDIR}/mastrms/mastrms/app/static/js/*.js ${TOPDIR}/mastrms/mastrms/app/static/js/repo/*.js"
    for JS in $JSFILES
    do
        java -jar ${CLOSURE} --js $JS --js_output_file output.js --warning_level DEFAULT --summary_detail_level 3
    done
}

installapp() {
    # check requirements
    which virtualenv >/dev/null

    log_info "Install ${PROJECT_NICKNAME}"
    virtualenv --system-site-packages ${TOPDIR}/virt_${PROJECT_NICKNAME}
    pushd ${TOPDIR}/${PROJECT_NICKNAME}
    ../virt_${PROJECT_NICKNAME}/bin/pip install ${PIP_OPTS} -e .
    popd
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/pip install ${PIP_OPTS} -r requirements/dev.txt
}


# django syncdb, migrate and collect static
syncmigrate() {
    log_info "syncdb"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> syncdb-develop.log
    log_info "migrate"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py migrate --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> migrate-develop.log
    log_info "collectstatic"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} --traceback 1> collectstatic-develop.log
}

startserver() {
    log_info "Starting server on http://$(hostname -I):${PORT}"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py runserver_plus 0.0.0.0:${PORT} --traceback
}

pythonversion() {
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/python -V
}

pipfreeze() {
    log_info "${PROJECT_NICKNAME} pip freeze"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/pip freeze
}

clean() {
    log_info "Cleaning"
    find ${TOPDIR}/${PROJECT_NICKNAME} -name "*.pyc" -exec rm -rf {} \;
}

purge() {
    log_info "Purging"
    rm -rf ${TOPDIR}/virt_${PROJECT_NICKNAME}
    rm *.log
}


load_base() {
    # BASE Controlled Vocabularies
    python manage.py loaddata ./apps/BASE/fixtures/LandUseCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/TargetGeneCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/TargetCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/PCRPrimerCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/GeneralEcologicalZoneCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/BroadVegetationTypeCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/TillageCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/HorizonCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/SoilClassificationCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/ProfilePositionCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/DrainageClassificationCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/SoilColourCV.json  --traceback
    python manage.py loaddata ./apps/BASE/fixtures/SoilTextureCV.json  --traceback

    python manage.py runscript ingest_BASE --traceback
}

devrun() {
    python manage.py syncdb --traceback --noinput
    python manage.py migrate --traceback

    python manage.py runscript set_initial_bpa_projects --traceback
    python manage.py runscript ingest_users --traceback
    #python manage.py runscript ingest_melanoma --traceback
    #python manage.py runscript ingest_gbr --traceback
    python manage.py runscript ingest_wheat_pathogens --traceback

    # load_base

    startserver
}

dev() { 
    devsettings
    devrun
}

wheat_pathogens_dev() {
    devsettings
    python manage.py syncdb --traceback --noinput
    python manage.py migrate --traceback

    python manage.py runscript set_initial_bpa_projects --traceback
    python manage.py runscript ingest_users --traceback
    python manage.py runscript ingest_wheat_pathogens --traceback
}


install_ccg() {
    TGT=/usr/local/bin/ccg
    log_info "Installing CCG to ${TGT}"
    wget https://bitbucket.org/ccgmurdoch/ccg/raw/default/ccg -O ${TGT}
    chmod 755 ${TGT}
}

flushdb() {
    DB="bpam"
    log_info "Flushing ${DB}"
    mysql -u ${DB} -p${DB} -e "DROP DATABASE ${DB}"
    mysql -u ${DB} -p${DB} -e "CREATE DATABASE ${DB}"
}

coverage() {
    log_info "Running coverage with reports"
    coverage `run ../manage.py test --settings=bpam.nsettings.test --traceback`
    coverage html --include=" $ SITE_URL*" --omit="admin.py"
}

unittest() {
    log_info "Running Unit Test"
    python manage.py test --settings=bpam.nsettings.test --traceback
}


nuclear() {
   CMD='python manage.py'
   ${CMD} reset_db --router=default --traceback
   ${CMD} syncdb --noinput --traceback
   ${CMD} migrate --traceback
   ${CMD} runscript set_initial_bpa_projects --traceback
   ${CMD} runscript ingest_users --script-args ../data/users/current
   ${CMD} runscript ingest_gbr --script-args ../data/gbr/current
   ${CMD} runscript ingest_melanoma --script-args ../data/melanoma/current
   ${CMD} runscript ingest_wheat_pathogens --script-args ../data/wheat_pathogens/current
   ${CMD} runscript ingest_wheat_cultivars --script-args ../data/wheat_cultivars/current
}

usage() {
    log_warning "Usage ./develop.sh (lint|jslint)"
    log_warning "Usage ./develop.sh (flushdb)"
    log_warning "Usage ./develop.sh (unittest|coverage)"
    log_warning "Usage ./develop.sh (start|install|clean|purge|pipfreeze|pythonversion)"
    log_warning "Usage ./develop.sh (ci_remote_build|ci_staging|ci_rpm_publish|ci_remote_destroy)"
    log_warning "Usage ./develop.sh (nuclear)"
    log_warning "Usage ./develop.sh (wheat_pathogens_dev)"
}


case ${ACTION} in
    coverage)
        coverage
        ;;
    wheat_pathogens_dev)
        wheat_pathogens_dev
        ;;
    unittest)
        unittest
        ;;
    flushdb)
	    flushdb
        ;;
    nuclear)
	    nuclear
        ;;
    pythonversion)
        pythonversion
        ;;
    install_ccg)
        install_ccg
        ;;
    pipfreeze)
        pipfreeze
        ;;
    lint)
        lint
        ;;
    jslint)
        jslint
        ;;
    syncmigrate)
        devsettings
        syncmigrate
        ;;
    start)
        devsettings
        startserver
        ;;
    install)
        devsettings
        installapp
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
    clean)
        settings
        clean
        ;;
    purge)
        settings
        clean
        purge
        ;;
    dev)
        dev
        ;;
    *)
        usage
esac
