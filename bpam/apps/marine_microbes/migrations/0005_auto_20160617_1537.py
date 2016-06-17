# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0004_auto_20160617_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='extraction',
            field=models.IntegerField(default=1, verbose_name=b'Extraction'),
        ),
        migrations.AddField(
            model_name='metagenomisequencefile',
            name='vendor',
            field=models.CharField(default=b'UNKNOWN', max_length=100, verbose_name=b'Vendor'),
        ),
    ]
