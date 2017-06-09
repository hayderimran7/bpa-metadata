# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0030_auto_20170602_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amplicon16strack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='amplicon18strack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='amplicona16strack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='metagenomicstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='metatranscriptometrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
    ]
