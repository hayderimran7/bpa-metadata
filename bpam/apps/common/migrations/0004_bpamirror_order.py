# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('common', '0003_bpamirror'), ]

    operations = [
        migrations.AddField(model_name='bpamirror',
                            name='order',
                            field=models.IntegerField(default=99, unique=True),
                            preserve_default=False, ),
    ]
