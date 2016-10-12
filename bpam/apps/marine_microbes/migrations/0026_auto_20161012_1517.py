# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0025_auto_20161005_1125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metagenomicsequencefile',
            options={'verbose_name_plural': 'Metagenome Sequence Files'},
        ),
    ]
