# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_contextual', '0004_auto_20150525_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionsite',
            name='crop_rotation_1',
            field=models.TextField(null=True, verbose_name='Crop rotation 1 year ago', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collectionsite',
            name='crop_rotation_2',
            field=models.TextField(null=True, verbose_name='Crop rotation 2 years ago', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collectionsite',
            name='crop_rotation_3',
            field=models.TextField(null=True, verbose_name=b'Crop rotation 3 years ago', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collectionsite',
            name='crop_rotation_4',
            field=models.TextField(null=True, verbose_name='Crop rotation 4 years ago', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collectionsite',
            name='crop_rotation_5',
            field=models.TextField(null=True, verbose_name='Crop rotation 5 years ago', blank=True),
            preserve_default=True,
        ),
    ]
