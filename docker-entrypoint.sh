#!/bin/bash

COMMAND=$1

# wait for a given host:port to become available
dockerwait() {
    host=$1
    port=$2
    while ! exec 6<>/dev/tcp/${host}/${port}
    do
        echo "$(date) - waiting to connect ${host} ${port}"
        sleep 5
    done
    echo "$(date) - connected to $host $port"

    exec 6>&-
    exec 6<&-
}


# wait for services to become available
# this prevents race conditions using fig
wait_for_services() {
    if [[ "$WAIT_FOR_QUEUE" ]] ; then
        dockerwait $QUEUESERVER $QUEUEPORT
    fi
    if [[ "$WAIT_FOR_DB" ]] ; then
        dockerwait $DBSERVER $DBPORT
    fi
    if [[ "$WAIT_FOR_CACHE" ]] ; then
        dockerwait $CACHESERVER $CACHEPORT
    fi
    if [[ "$WAIT_FOR_WEB" ]] ; then
        dockerwait $WEBSERVER $WEBPORT
    fi
}


defaults() {

    : ${ENV_PATH:="/env/bin"}

    : ${DBSERVER:="db"}
    : ${DBPORT:="5432"}
    : ${WEBSERVER="web"}
    : ${WEBPORT="8000"}
    : ${CACHESERVER="cache"}
    : ${CACHEPORT="11211"}

    : ${DBUSER="webapp"}
    : ${DBNAME="${DBUSER}"}
    : ${DBPASS="${DBUSER}"}

    . ${ENV_PATH}/activate

    export DBSERVER DBPORT DBUSER DBNAME DBPASS
}


django_defaults() {
    : ${DEPLOYMENT="dev"}
    : ${PRODUCTION=0}
    : ${DEBUG=1}
    : ${MEMCACHE="${CACHESERVER}:${CACHEPORT}"}
    : ${WRITABLE_DIRECTORY="/data/scratch"}
    : ${STATIC_ROOT="/data/static"}
    : ${MEDIA_ROOT="/data/static/media"}
    : ${LOG_DIRECTORY="/data/log"}
    : ${DJANGO_SETTINGS_MODULE="bpam.settings"}

    echo "DEPLOYMENT is ${DEPLOYMENT}"
    echo "PRODUCTION is ${PRODUCTION}"
    echo "DEBUG is ${DEBUG}"
    echo "MEMCACHE is ${MEMCACHE}"
    echo "WRITABLE_DIRECTORY is ${WRITABLE_DIRECTORY}"
    echo "STATIC_ROOT is ${STATIC_ROOT}"
    echo "MEDIA_ROOT is ${MEDIA_ROOT}"
    echo "LOG_DIRECTORY is ${LOG_DIRECTORY}"
    echo "DJANGO_SETTINGS_MODULE is ${DJANGO_SETTINGS_MODULE}"
    export DEPLOYMENT PRODUCTION DEBUG DBSERVER MEMCACHE WRITABLE_DIRECTORY STATIC_ROOT MEDIA_ROOT LOG_DIRECTORY DJANGO_SETTINGS_MODULE
}

echo "HOME is ${HOME}"
echo "WHOAMI is $(whoami)"

defaults
django_defaults
wait_for_services


# BASE
ingest_base() {
    django-admin.py runscript ingest_base_454 --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_metagenomics --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_landuse --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_contextual --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_amplicon --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_sra_id--traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_base_otu --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
}

# Great Barrier Reef
ingest_gbr() {
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_gbr_metagenomics --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_gbr_amplicons --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    # django-admin.py runscript ingest_gbr_smrt --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
}

make_migrations() {
    django-admin.py makemigrations bpaauth --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations common --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base_metagenomics --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base_amplicon --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base_contextual --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base_otu --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations base_454 --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations melanoma --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations gbr --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations gbr_amplicon --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations wheat_pathogens --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations wheat_pathogens_transcript --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations wheat_cultivars --traceback --settings=${DJANGO_SETTINGS_MODULE}
    django-admin.py makemigrations barcode --traceback --settings=${DJANGO_SETTINGS_MODULE}
}

if [ "${COMMAND}" = 'nuclear' ]
then
    django-admin.py reset_db --router=default --traceback --settings=${DJANGO_SETTINGS_MODULE}
    make_migrations
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    exit $?
fi

if [ "${COMMAND}" = 'runscript' ]
then
    echo "Runscript $2"
    django-admin.py runscript $2 --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runscript.log
    exit $?
fi

if [ "${COMMAND}" = 'ingest_all' ]
then
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log

    django-admin.py runscript ingest_bpa_projects --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    # django-admin.py runscript ingest_users --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_melanoma --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_wheat_pathogens --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_wheat_pathogens_transcript --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log
    django-admin.py runscript ingest_wheat_cultivars --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log

    ingest_gbr
    ingest_base

    # links
    django-admin.py runscript url_checker --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/ingest.log

    exit $?
fi

if [ "${COMMAND}" = 'ingest_gbr' ]
then
    ingest_gbr
    exit $?
fi

if [ "${COMMAND}" = 'ingest_base' ]
then
    ingest_base
    exit $?
fi

if [ "${COMMAND}" = 'admin' ]
then
    echo "admin"
    if [ "$2" = "" ]
    then 
        admincmd="help"
    else
        admincmd=$2
    fi
    django-admin.py $admincmd --settings=${DJANGO_SETTINGS_MODULE}
    exit $?
fi

# set superuser 
if [ "${COMMAND}" = 'superuser' ]
then
    echo "Setting superuser (admin)"
    django-admin.py  createsuperuser --email="admin@ccg.com" --settings=${DJANGO_SETTINGS_MODULE}
    exit $?
fi

# security by django checksecure
if [ "$COMMAND" = 'checksecure' ]
then
    echo "[Run] Running Django checksecure"
    django-admin.py checksecure --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/checksecure.log

    exit $?
fi

# uwsgi entrypoint
if [ "$COMMAND" = 'uwsgi' ]
then
    echo "[Run] Starting uwsgi"

    : ${UWSGI_OPTS="/app/uwsgi/docker.ini"}
    echo "UWSGI_OPTS is ${UWSGI_OPTS}"

    django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/uwsgi-collectstatic.log
    django-admin.py syncdb --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/uwsgi-syncdb.log
    django-admin.py migrate --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/uwsgi-migrate.log
    exec uwsgi --die-on-term --ini ${UWSGI_OPTS}
fi

# runserver entrypoint
if [ "$COMMAND" = 'runserver' ]
then
    echo "[Run] Starting runserver"

    : ${RUNSERVER_OPTS="runserver_plus 0.0.0.0:${WEBPORT} --settings=${DJANGO_SETTINGS_MODULE}"}
    echo "RUNSERVER_OPTS is ${RUNSERVER_OPTS}"

    echo "Django collectstatic"
    django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runserver-collectstatic.log
    echo "Django migrate"
    django-admin.py migrate auth --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runserver-migrate.log
    django-admin.py migrate --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/runserver-migrate.log

    echo "Django runserver"
    exec django-admin.py ${RUNSERVER_OPTS}
fi

# runtests entrypoint
if [ "$COMMAND" = 'runtests' ] 
then
    echo "Django test"
    cd /app/bpam
    exec django-admin.py test --traceback --settings=${DJANGO_SETTINGS_MODULE}
fi

# lettuce entrypoint
if [ "$COMMAND" = 'lettuce' ]
then
    echo "[Run] Starting lettuce"
    exec django-admin.py run_lettuce --with-xunit --xunit-file=/data/tests.xml
fi

# prepare a tarball of build
if [ "$COMMAND" = 'tarball' ]
then
    echo "[Run] Preparing a tarball of build"

    cd /app
    rm -rf /app/*
    echo $GIT_TAG
    set -x
    git clone --depth=1 --branch=$GIT_TAG https://github.com/muccg/bpa-metadata.git .

    # install python deps
    # Note: Environment vars are used to control the behaviour of pip (use local devpi for instance)
    pip install ${PIP_OPTS} --upgrade -r requirements/runtime-requirements.txt
    # going to move this one up
    pip install -e ./bpam/
    set +x
    
    # create release tarball
    DEPS="/env /app/uwsgi /app/docker-entrypoint.sh /app/bpam"
    cd /data
    exec tar -cpzf bpametadata-${GIT_TAG}.tar.gz ${DEPS}
fi

echo "[RUN]: Builtin command not provided [lettuce|runtests|runserver|uwsgi|checksecure|superuser|nuclear|ingest|runscript]"
echo "[RUN]: $@"

exec "$@"
