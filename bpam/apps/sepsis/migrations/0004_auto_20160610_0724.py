# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0003_auto_20160610_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growthmethod',
            name='growth_condition_time',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Growth condition time', blank=True),
        ),
        migrations.AlterField(
            model_name='growthmethod',
            name='note',
            field=models.TextField(max_length=500, null=True, verbose_name=b'Note', blank=True),
        ),
    ]
