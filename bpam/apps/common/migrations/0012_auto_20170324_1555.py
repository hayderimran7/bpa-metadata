# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_ckanserver_api_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ckanserver',
            options={'ordering': ['order'], 'verbose_name': 'CKAN Server'},
        ),
    ]
