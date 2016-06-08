# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0003_auto_20160602_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sepsissample',
            old_name='growt_method',
            new_name='growth_method',
        ),
    ]
