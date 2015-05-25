# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_contextual', '0003_samplecontext_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionsite',
            name='date_since_change_in_land_use',
            field=models.CharField(max_length=100, null=True, verbose_name='Date Since Land Use Change', blank=True),
            preserve_default=True,
        ),
    ]
