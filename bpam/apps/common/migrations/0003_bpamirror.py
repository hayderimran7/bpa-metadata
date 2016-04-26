# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_bpauniqueid_sra_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPAMirror',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('base_url', models.URLField()),
            ],
        ),
    ]
