# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0027_auto_20161117_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='genomicsmiseqtrack',
            name='growth_condition_notes',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Growth condition notes', blank=True),
        ),
        migrations.AddField(
            model_name='genomicspacbiotrack',
            name='growth_condition_notes',
            field=models.CharField(max_length=500, null=True, verbose_name=b'Growth condition notes', blank=True),
        ),
    ]
