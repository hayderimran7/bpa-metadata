# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('marine_microbes', '0006_auto_20160617_1552'), ]

    operations = [
        migrations.RemoveField(model_name='metagenomisequencefile',
                               name='runsamplenum', ),
    ]
