# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_delete_site'),
    ]

    operations = [
        migrations.CreateModel(
            name='CKANServer',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('base_url', models.URLField()),
                ('order', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
