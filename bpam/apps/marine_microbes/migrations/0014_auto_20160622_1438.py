# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0013_remove_ampliconsequencefile_lane'),
    ]

    operations = [
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='sample',
            field=models.ForeignKey(to='marine_microbes.MMSample', null=True),
        ),
        migrations.AlterField(
            model_name='metagenomicsequencefile',
            name='sample',
            field=models.ForeignKey(to='marine_microbes.MMSample', null=True),
        ),
    ]
