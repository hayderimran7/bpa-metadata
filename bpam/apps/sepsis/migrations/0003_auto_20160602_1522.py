# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0002_auto_20160602_1206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transcriptomicsmethod',
            options={'verbose_name': 'Transcriptomics Method'},
        ),
        migrations.AddField(
            model_name='transcriptomicsmethod',
            name='casava_version',
            field=models.CharField(max_length=20, null=True, verbose_name=b'CASAVA Version', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptomicsmethod',
            name='insert_size_range',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Insert Size Range', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptomicsmethod',
            name='library_construction_protocol',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Library Construction Protocol', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptomicsmethod',
            name='sequencer',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Sequencer', blank=True),
        ),
    ]
