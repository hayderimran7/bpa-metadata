#!/bin/bash

python manage.py syncdb --settings=bpametadata.settings.dev
python manage.py runscript ingest --settings=bpametadata.settings.dev
python manage.py runserver --settings=bpametadata.settings.dev
