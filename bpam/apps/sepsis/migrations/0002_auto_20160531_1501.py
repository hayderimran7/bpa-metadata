# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genomicsmiseqfile',
            name='lane',
        ),
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='index_number',
            field=models.IntegerField(null=True, verbose_name=b'Index Number', blank=True),
        ),
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='lane_number',
            field=models.IntegerField(null=True, verbose_name=b'Lane Number', blank=True),
        ),
        migrations.AlterField(
            model_name='genomicsmiseqfile',
            name='read_number',
            field=models.IntegerField(null=True, verbose_name=b'Read Number', blank=True),
        ),
        migrations.AlterField(
            model_name='proteomicsfile',
            name='index_number',
            field=models.IntegerField(null=True, verbose_name=b'Index Number', blank=True),
        ),
        migrations.AlterField(
            model_name='proteomicsfile',
            name='lane_number',
            field=models.IntegerField(null=True, verbose_name=b'Lane Number', blank=True),
        ),
        migrations.AlterField(
            model_name='proteomicsfile',
            name='read_number',
            field=models.IntegerField(null=True, verbose_name=b'Read Number', blank=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsfile',
            name='index_number',
            field=models.IntegerField(null=True, verbose_name=b'Index Number', blank=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsfile',
            name='lane_number',
            field=models.IntegerField(null=True, verbose_name=b'Lane Number', blank=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsfile',
            name='read_number',
            field=models.IntegerField(null=True, verbose_name=b'Read Number', blank=True),
        ),
    ]
