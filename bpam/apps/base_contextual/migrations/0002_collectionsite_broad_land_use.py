# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_vocabulary', '0002_vocabulary'),
        ('base_contextual', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionsite',
            name='broad_land_use',
            field=models.ForeignKey(related_name='broad', verbose_name='Broad Land Use', to='base_vocabulary.LandUse', null=True),
            preserve_default=True,
        ),
    ]
