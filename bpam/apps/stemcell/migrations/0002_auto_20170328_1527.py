# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metabolomictrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='metabolomictrack',
            name='data_generated',
        ),
        migrations.RemoveField(
            model_name='proteomictrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='proteomictrack',
            name='data_generated',
        ),
        migrations.RemoveField(
            model_name='singlecellrnaseqtrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='singlecellrnaseqtrack',
            name='data_generated',
        ),
        migrations.RemoveField(
            model_name='smallrnatrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='smallrnatrack',
            name='data_generated',
        ),
        migrations.RemoveField(
            model_name='transcriptometrack',
            name='archive_ingestion_date',
        ),
        migrations.RemoveField(
            model_name='transcriptometrack',
            name='data_generated',
        ),
    ]
