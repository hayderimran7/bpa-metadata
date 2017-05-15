# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0005_auto_20170505_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='metabolomictrack',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Research Group', blank=True),
        ),
        migrations.AddField(
            model_name='proteomictrack',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Research Group', blank=True),
        ),
        migrations.AddField(
            model_name='singlecellrnaseqtrack',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Research Group', blank=True),
        ),
        migrations.AddField(
            model_name='smallrnatrack',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Research Group', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptometrack',
            name='group',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Research Group', blank=True),
        ),
        migrations.AlterField(
            model_name='metabolomictrack',
            name='data_set_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set ID', blank=True),
        ),
        migrations.AlterField(
            model_name='proteomictrack',
            name='data_set_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set ID', blank=True),
        ),
        migrations.AlterField(
            model_name='singlecellrnaseqtrack',
            name='data_set_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set ID', blank=True),
        ),
        migrations.AlterField(
            model_name='smallrnatrack',
            name='data_set_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set ID', blank=True),
        ),
        migrations.AlterField(
            model_name='transcriptometrack',
            name='data_set_id',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set ID', blank=True),
        ),
    ]
