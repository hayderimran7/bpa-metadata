# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0009_auto_20160519_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='strain_or_isolate',
            field=models.CharField(max_length=200, unique=True, null=True, verbose_name=b'Strain Or Isolate', blank=True),
        ),
    ]
