#!/bin/bash

DEV_SETTINGS=bpametadata.settings.dev
DEMO_SETTINGS=bpametadata.settings.demo

run() {
    python manage.py syncdb --settings=$1 --traceback
    python manage.py runscript ingest --settings=$1 --traceback
    python manage.py runserver --settings=$1
}


dev() {
    rm /tmp/bpa*
    run ${DEV_SETTINGS}
}

demo() {
    rm /tmp/demobpa*
    run ${DEMO_SETTINGS}
}

dev