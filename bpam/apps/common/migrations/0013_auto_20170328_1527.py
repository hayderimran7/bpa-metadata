# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_auto_20170324_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bpauniqueid',
            options={'verbose_name': 'BPA Unique ID', 'verbose_name_plural': 'BPA Unique IDs'},
        ),
    ]
