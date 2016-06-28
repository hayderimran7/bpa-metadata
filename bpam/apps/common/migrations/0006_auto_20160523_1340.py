# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('common', '0005_auto_20160427_1509'), ]

    operations = [
        migrations.AlterField(
            model_name='bpauniqueid',
            name='project',
            field=models.ForeignKey(related_name='bpa_ids', to='common.BPAProject'), ),
    ]
