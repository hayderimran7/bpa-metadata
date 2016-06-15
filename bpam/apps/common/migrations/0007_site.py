# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20160523_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True, verbose_name=b'Location Description')),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text=b'Represented as (longitude, latitude)', srid=4326, verbose_name=b'Position')),
                ('note', models.TextField(null=True, verbose_name=b'Note', blank=True)),
            ],
            options={
                'verbose_name': 'Sample Site',
                'verbose_name_plural': 'Sample Sites',
            },
        ),
    ]
