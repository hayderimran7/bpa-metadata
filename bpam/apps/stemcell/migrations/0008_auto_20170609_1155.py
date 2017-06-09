# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0007_auto_20170608_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metabolomictrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='proteomictrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='singlecellrnaseqtrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='smallrnatrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
        migrations.AlterField(
            model_name='transcriptometrack',
            name='in_data_portal',
            field=models.BooleanField(default=False, verbose_name=b'Data ingested into data portal'),
        ),
    ]
