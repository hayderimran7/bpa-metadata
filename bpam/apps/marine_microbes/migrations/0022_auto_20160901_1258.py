# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0021_auto_20160830_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mmsite',
            name='name',
            field=models.TextField(verbose_name=b'Location Description'),
        ),
        migrations.AlterUniqueTogether(
            name='mmsite',
            unique_together=set([('name', 'point')]),
        ),
    ]
