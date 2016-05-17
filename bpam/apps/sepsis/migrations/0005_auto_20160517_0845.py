# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0004_sampletrack'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sampletrack',
            old_name='date_allocated',
            new_name='allocation_date',
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='archive_ingestion_date',
            field=models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Archive Ingestion Date', blank=True),
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='curation_url',
            field=models.URLField(null=True, verbose_name=b'Curation URL', blank=True),
        ),
        migrations.AddField(
            model_name='sampletrack',
            name='dataset_url',
            field=models.URLField(null=True, verbose_name=b'Dataset URL', blank=True),
        ),
    ]
