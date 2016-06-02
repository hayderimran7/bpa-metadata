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
            name='plate',
        ),
        migrations.AddField(
            model_name='genomicsmiseqfile',
            name='flow_cell_id',
            field=models.CharField(default='', max_length=6, verbose_name=b'Flow Cell ID'),
            preserve_default=False,
        ),
    ]
