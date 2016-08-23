# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0014_auto_20160823_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampletrack',
            name='facility',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Facility', blank=True),
        ),
    ]
