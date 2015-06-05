# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_metagenomics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metagenomicssequencefile',
            name='index',
            field=models.CharField(max_length=32, null=True, verbose_name='Index', blank=True),
            preserve_default=True,
        ),
    ]
