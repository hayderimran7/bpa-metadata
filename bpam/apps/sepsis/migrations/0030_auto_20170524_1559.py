# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0029_auto_20170524_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='genomicsmiseqtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genomicspacbiotrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metabolomicslcmstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteomicsms1quantificationtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proteomicsswathmstrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transcriptomicshiseqtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
            preserve_default=False,
        ),
    ]
