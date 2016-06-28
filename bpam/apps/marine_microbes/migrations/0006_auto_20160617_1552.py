# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('marine_microbes', '0005_auto_20160617_1537'), ]

    operations = [
        migrations.AlterField(model_name='metagenomisequencefile',
                              name='flow_cell_id',
                              field=models.CharField(max_length=9, verbose_name=b'Flow Cell ID'), ),
    ]
