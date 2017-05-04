# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stemcell', '0003_auto_20170328_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='metabolomictrack',
            name='cell_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Cell Type', blank=True),
        ),
        migrations.AddField(
            model_name='metabolomictrack',
            name='data_set',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set', blank=True),
        ),
        migrations.AddField(
            model_name='metabolomictrack',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Stem Cell State', blank=True),
        ),
        migrations.AddField(
            model_name='proteomictrack',
            name='cell_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Cell Type', blank=True),
        ),
        migrations.AddField(
            model_name='proteomictrack',
            name='data_set',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set', blank=True),
        ),
        migrations.AddField(
            model_name='proteomictrack',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Stem Cell State', blank=True),
        ),
        migrations.AddField(
            model_name='singlecellrnaseqtrack',
            name='cell_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Cell Type', blank=True),
        ),
        migrations.AddField(
            model_name='singlecellrnaseqtrack',
            name='data_set',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set', blank=True),
        ),
        migrations.AddField(
            model_name='singlecellrnaseqtrack',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Stem Cell State', blank=True),
        ),
        migrations.AddField(
            model_name='smallrnatrack',
            name='cell_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Cell Type', blank=True),
        ),
        migrations.AddField(
            model_name='smallrnatrack',
            name='data_set',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set', blank=True),
        ),
        migrations.AddField(
            model_name='smallrnatrack',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Stem Cell State', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptometrack',
            name='cell_type',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Cell Type', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptometrack',
            name='data_set',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Data Set', blank=True),
        ),
        migrations.AddField(
            model_name='transcriptometrack',
            name='state',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Stem Cell State', blank=True),
        ),
    ]
