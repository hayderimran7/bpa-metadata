# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sepsis', '0015_auto_20160823_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampletrack',
            name='data_generated',
            field=models.NullBooleanField(default=False, verbose_name=b'Data Generated'),
        ),
    ]
