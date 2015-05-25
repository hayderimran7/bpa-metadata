# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_contextual', '0002_collectionsite_broad_land_use'),
    ]

    operations = [
        migrations.AddField(
            model_name='samplecontext',
            name='storage',
            field=models.CharField(help_text='Storage', max_length=100, null=True, verbose_name='Storage', blank=True),
            preserve_default=True,
        ),
    ]
