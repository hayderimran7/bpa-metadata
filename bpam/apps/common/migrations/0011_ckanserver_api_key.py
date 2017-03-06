# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_ckanserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='ckanserver',
            name='api_key',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
