# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0010_auto_20160815_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacbiogenomicsmethod',
            name='insert_size_range',
            field=models.CharField(max_length=40, null=True, verbose_name=b'Insert Size Range', blank=True),
        ),
        migrations.AlterField(
            model_name='pacbiogenomicsmethod',
            name='library_construction_protocol',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Library Construction Protocol', blank=True),
        ),
        migrations.AlterField(
            model_name='pacbiogenomicsmethod',
            name='sequencer',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Sequencer', blank=True),
        ),
    ]
