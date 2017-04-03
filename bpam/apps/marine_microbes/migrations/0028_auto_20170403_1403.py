# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marine_microbes', '0027_auto_20161025_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transferlog',
            name='facility',
        ),
        migrations.DeleteModel(
            name='TransferLog',
        ),
    ]
