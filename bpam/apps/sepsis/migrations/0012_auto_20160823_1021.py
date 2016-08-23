# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0011_auto_20160823_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacbiogenomicsmethod',
            name='rs_version',
            field=models.CharField(max_length=100, null=True, verbose_name=b'RS Version', blank=True),
        ),
        migrations.AlterField(
            model_name='pacbiogenomicsmethod',
            name='sequencer_run_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Sequencer run ID', blank=True),
        ),
    ]
