# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0013_auto_20160823_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampletrack',
            name='bpa_id',
            field=models.CharField(max_length=6, verbose_name=b'BPA ID'),
        ),
    ]
