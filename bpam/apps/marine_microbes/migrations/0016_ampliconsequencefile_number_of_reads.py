# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0015_auto_20160623_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='number_of_reads',
            field=models.IntegerField(null=True, verbose_name=b'Number of Reads', blank=True),
        ),
    ]
