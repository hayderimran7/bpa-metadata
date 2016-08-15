# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0009_auto_20160815_1056'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='host_associated',
            new_name='associated',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_disease_status',
            new_name='disease_status',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_health_state',
            new_name='health_state',
        ),
    ]
