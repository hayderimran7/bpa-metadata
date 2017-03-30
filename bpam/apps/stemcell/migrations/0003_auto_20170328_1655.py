# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0002_auto_20170328_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='metabolomictrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
        migrations.AddField(
            model_name='proteomictrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
        migrations.AddField(
            model_name='singlecellrnaseqtrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
        migrations.AddField(
            model_name='smallrnatrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
        migrations.AddField(
            model_name='transcriptometrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
    ]
