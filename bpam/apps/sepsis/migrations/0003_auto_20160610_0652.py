# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('sepsis', '0002_sampletrack_bpa_id'), ]

    operations = [
        migrations.AlterField(
            model_name='growthmethod',
            name='growth_condition_time',
            field=models.CharField(
                max_length=200, null=True, verbose_name=b'Growth condition time',
                blank=True), ),
    ]
