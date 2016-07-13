#!/bin/bash

INGEST_LOG_FILE=/data/ingest.log
MIGRATE_LOG_FILE=/data/migrate.log

# wait for a given host:port to become available
#
# $1 host
# $2 port
function dockerwait {
    while ! exec 6<>/dev/tcp/$1/$2; do
        echo "$(date) - waiting to connect $1 $2"
        sleep 5
    done
    echo "$(date) - connected to $1 $2"

    exec 6>&-
    exec 6<&-
}


# wait for services to become available
# this prevents race conditions using fig
function wait_for_services() {
    if [[ "$WAIT_FOR_DB" ]] ; then
        dockerwait $DBSERVER $DBPORT
    fi
    if [[ "$WAIT_FOR_CACHE" ]] ; then
        dockerwait $CACHESERVER $CACHEPORT
    fi
    if [[ "$WAIT_FOR_RUNSERVER" ]] ; then
        dockerwait $RUNSERVER $RUNSERVERPORT
    fi
    if [[ "$WAIT_FOR_HOST_PORT" ]]; then
        dockerwait $DOCKER_ROUTE $WAIT_FOR_HOST_PORT
    fi
}


function defaults() {
    : ${DBSERVER:="db"}
    : ${DBPORT:="5432"}
    : ${DBUSER="webapp"}
    : ${DBNAME="${DBUSER}"}
    : ${DBPASS="${DBUSER}"}

    : ${DOCKER_ROUTE:=$(/sbin/ip route|awk '/default/ { print $3 }')}

    : ${RUNSERVER="web"}
    : ${RUNSERVERPORT="8000"}
    : ${CACHESERVER="cache"}
    : ${CACHEPORT="11211"}
    : ${MEMCACHE:="${CACHESERVER}:${CACHEPORT}"}

    export DBSERVER DBPORT DBUSER DBNAME DBPASS MEMCACHE DOCKER_ROUTE
}


function selenium_defaults {
    : ${SELENIUM_URL:="http://$DOCKER_ROUTE:$RUNSERVERPORT/"}
    #: ${SELENIUM_BROWSER:="*googlechrome"}
    : ${SELENIUM_BROWSER:="*firefox"}

    if [ ${DEPLOYMENT} = "prod" ]; then
        SELENIUM_URL="https://$DOCKER_ROUTE:8443/app/"
    fi

    export SELENIUM_URL SELENIUM_BROWSER
}


function _django_migrate {
    echo "running migrate"
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${MIGRATE_LOG_FILE}
}


function _django_collectstatic {
    echo "running collectstatic"
    django-admin.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/collectstatic.log
}


# BASE
function ingest_base() {
    django-admin.py set_vocabulary --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_454 --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_metagenomics --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_landuse --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_contextual --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_amplicon --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_sra_id--traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py base_ingest_otu --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
}


# Great Barrier Reef
function ingest_gbr() {
    django-admin.py gbr_ingest_metagenomics --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py gbr_ingest_amplicons --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
}


trap exit SIGHUP SIGINT SIGTERM
defaults
env | grep -iv PASS | sort
wait_for_services


# reset database and perform all migrations
if [ "$1" = 'nuclear' ]; then
    django-admin.py reset_db --router=default --traceback --settings=${DJANGO_SETTINGS_MODULE}
    make_migrations
    exec django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
fi

# ingest all bpa project data
if [ "$1" = 'ingest_all' ]; then
    django-admin.py migrate --traceback --settings=${DJANGO_SETTINGS_MODULE} --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}

    django-admin.py ingest_bpa_projects --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py melanoma_ingest --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py wheat_pathogens_ingest --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py wheat_pathogens_transcript_ingest --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
    django-admin.py wheat_cultivars_ingest --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}

    ingest_gbr
    ingest_base

    # links
    exec django-admin.py url_checker --traceback --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee ${INGEST_LOG_FILE}
fi

# ingest gbr
if [ "$1" = 'ingest_gbr' ]; then
    ingest_gbr
    exit $?
fi

# ingest base
if [ "$1" = 'ingest_base' ]; then
    ingest_base
    exit $?
fi

# security by django checksecure
if [ "$1" = 'checksecure' ]; then
    echo "[Run] Running Django checksecure"
    exec django-admin.py checksecure --traceback 2>&1 | tee /data/checksecure.log
fi

# uwsgi entrypoint
if [ "$1" = 'uwsgi' ]; then
    echo "[Run] Starting uwsgi"

    : ${UWSGI_OPTS="/app/uwsgi/docker.ini"}
    echo "UWSGI_OPTS is ${UWSGI_OPTS}"

     _django_collectstatic
     _django_migrate

    exec uwsgi --die-on-term --ini ${UWSGI_OPTS}
fi

# runserver entrypoint
if [ "$1" = 'runserver' ]; then
    echo "[Run] Starting runserver"

    : ${RUNSERVER_OPTS="runserver_plus 0.0.0.0:${RUNSERVERPORT} --settings=${DJANGO_SETTINGS_MODULE}"}
    echo "RUNSERVER_OPTS is ${RUNSERVER_OPTS}"

     _django_collectstatic

     # some one off bpa goop
     #django-admin.py migrate auth --noinput --settings=${DJANGO_SETTINGS_MODULE} 2>&1 | tee /data/migrate.log

     _django_migrate

    echo "running runserver ..."
    exec django-admin.py ${RUNSERVER_OPTS}
fi

# runtests entrypoint
if [ "$1" = 'runtests' ]; then
    echo "[Run] Starting tests"
    exec django-admin.py test --traceback
fi

# lettuce entrypoint
if [ "$1" = 'lettuce' ]; then
    echo "[Run] Starting lettuce"
    exec django-admin.py run_lettuce --with-xunit --xunit-file=/data/tests.xml
fi

# prepare a tarball of build
if [ "$1" = 'tarball' ]; then
    echo "[Run] Preparing a tarball of build"

    cd /app
    rm -rf /app/*
    echo $GIT_TAG
    set -x
    git clone --depth=1 --branch=$GIT_TAG ${PROJECT_SOURCE} .
    git ls-remote ${PROJECT_SOURCE} ${GIT_TAG} > .version

    # install python deps
    # Note: Environment vars are used to control the behaviour of pip (use local devpi for instance)
    pip install ${PIP_OPTS} --upgrade -r requirements/runtime-requirements.txt
    pip install -e bpam
    set +x
    # create release tarball
    DEPS="/env /app/uwsgi /app/docker-entrypoint.sh /app/bpam"
    cd /data
    exec tar -cpzf ${PROJECT_NAME}-${GIT_TAG}.tar.gz ${DEPS}
fi

echo "[RUN]: Builtin command not provided [lettuce|runtests|runserver|uwsgi|checksecure|superuser|nuclear|ingest]"
echo "[RUN]: Many management commands are available from django-admin.py "
echo "[RUN]: e.g by running /app/docker-entrypoint.sh django-admin.py url_checker from a docker exec session"
echo "[RUN]: $@"

exec "$@"
