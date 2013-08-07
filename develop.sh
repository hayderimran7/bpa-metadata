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
AWS_STAGING_INSTANCE='aws_syd_bpam_staging'
TARGET_DIR="/usr/local/src/${PROJECT_NICKNAME}"
TESTING_MODULES="nose"
MODULES="MySQL-python==1.2.3 psycopg2==2.4.6 Werkzeug flake8 ${TESTING_MODULES}"
PIP_OPTS="-v -M --download-cache ~/.pip/cache"

devsettings() {
    export DJANGO_SETTINGS_MODULE="bpametadata.settings.dev"
}

demosettings() {
    export DJANGO_SETTINGS_MODULE="bpametadata.settings.demo"
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
    TIP=$(hg tip --template "{node}" 2>/dev/null || /bin/true)
    echo "# Generated by develop.sh"
    echo "build.timestamp=\"$DATE\""
    echo "build.tip=\"$TIP\""
}

# build RPMs on a remote host from ci environment
ci_remote_build() {
    time ccg ${AWS_BUILD_INSTANCE} boot
    time ccg ${AWS_BUILD_INSTANCE} puppet
    time ccg ${AWS_BUILD_INSTANCE} shutdown:50

    cd ${TOPDIR}

    if [ -z "$BAMBOO_BUILDKEY" ]; then
        # We aren't running under Bamboo, create new build-number.txt.
        build_number_head > build-number.txt
    else
        # Bamboo has already put some useful information in
        # build-number.txt, so append to it.
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
    time ccg ${AWS_BUILD_INSTANCE} publish_rpm:build/${PROJECT_NAME}*.rpm,release=6
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

    echo "Install ${PROJECT_NICKNAME}"
    virtualenv --system-site-packages ${TOPDIR}/virt_${PROJECT_NICKNAME}
    pushd ${TOPDIR}/${PROJECT_NICKNAME}
    ../virt_${PROJECT_NICKNAME}/bin/pip install ${PIP_OPTS} -e .
    popd
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/pip install ${PIP_OPTS} ${MODULES}
}


# django syncdb, migrate and collect static
syncmigrate() {
    echo "syncdb"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> syncdb-develop.log
    echo "migrate"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py migrate --settings=${DJANGO_SETTINGS_MODULE} 1> migrate-develop.log
    echo "collectstatic"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 1> collectstatic-develop.log
}

# start runserver
startserver() {
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/django-admin.py runserver_plus ${port}
}

pythonversion() {
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/python -V
}

pipfreeze() {
    echo "${PROJECT_NICKNAME} pip freeze"
    ${TOPDIR}/virt_${PROJECT_NICKNAME}/bin/pip freeze
    echo ''
}

clean() {
    find ${TOPDIR}/${PROJECT_NICKNAME} -name "*.pyc" -exec rm -rf {} \;
}

purge() {
    rm -rf ${TOPDIR}/virt_${PROJECT_NICKNAME}
    rm *.log
}

run() {
    python manage.py syncdb --traceback
    python manage.py runscript ingest_melanoma --traceback
    python manage.py runserver
}

dev() {
    (
	cd ${PROJECT_NICKNAME}
        if [ -f /tmp/bpa* ]
	then
	    rm /tmp/bpa*
        fi
	devsettings
	run
    )
}

demo() {
    rm /tmp/demobpa*
    demosettings
    run
}

usage() {
    echo ""
    echo "Usage ./develop.sh (lint|jslint|start|install|clean|purge|pipfreeze|pythonversion|ci_remote_build|ci_staging|ci_rpm_publish|ci_remote_destroy)"
    echo ""
}

case ${ACTION} in
pythonversion)
    pythonversion
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
demo)
    demo
    ;;
*)
    usage
esac
