# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sepsissample',
            name='serovar',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Serovar', blank=True),
        ),
    ]
