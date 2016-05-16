# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0002_auto_20160516_1504'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sepsissample',
            old_name='collection_date',
            new_name='culture_collection_date',
        ),
    ]
