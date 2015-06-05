# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_metagenomics', '0002_metagenomicssequencefile_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='metagenomicssequencefile',
            name='read_number',
            field=models.IntegerField(null=True, verbose_name='Read', blank=True),
            preserve_default=True,
        ),
    ]
