# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0003_auto_20160513_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicsmethod',
            name='growth_condition_media',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True),
        ),
        migrations.AlterField(
            model_name='proteomicsmethod',
            name='growth_condition_media',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True),
        ),
        migrations.AlterField(
            model_name='transcriptomicsmethod',
            name='growth_condition_media',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True),
        ),
    ]
