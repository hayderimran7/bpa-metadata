#!/bin/bash

DEV_SETTINGS=bpametadata.settings.dev
rm /tmp/bpa*
python manage.py syncdb --settings=${DEV_SETTINGS} --traceback
python manage.py runscript ingest --settings=${DEV_SETTINGS} --traceback
python manage.py runserver --settings=${DEV_SETTINGS}
