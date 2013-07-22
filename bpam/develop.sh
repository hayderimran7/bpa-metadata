#!/bin/bash

DEV_SETTINGS=bpametadata.settings.dev

python manage.py syncdb --settings=${DEV_SETTINGS}
python manage.py runscript ingest --settings=${DEV_SETTINGS}
python manage.py runserver --settings=${DEV_SETTINGS}
