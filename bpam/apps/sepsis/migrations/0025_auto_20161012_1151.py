# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0024_auto_20160930_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='deeplcmstrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
        migrations.AddField(
            model_name='metabolomicstrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
        migrations.AddField(
            model_name='miseqtrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
        migrations.AddField(
            model_name='pacbiotrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
        migrations.AddField(
            model_name='rnahiseqtrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
        migrations.AddField(
            model_name='swathmstrack',
            name='data_type',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Data Type', choices=[(1, b'Pre-pilot'), (2, b'Pilot'), (3, b'Main dataset')]),
        ),
    ]
