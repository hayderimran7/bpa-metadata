# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0030_auto_20170524_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicsmiseqtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='genomicspacbiotrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='metabolomicslcmstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='proteomicsms1quantificationtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='proteomicsswathmstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='transcriptomicshiseqtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
    ]
