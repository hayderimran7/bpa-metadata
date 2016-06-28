# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('sepsis', '0004_auto_20160610_0724'), ]

    operations = [
        migrations.RemoveField(model_name='sepsissample',
                               name='id', ),
        migrations.AlterField(model_name='sepsissample',
                              name='bpa_id',
                              field=models.OneToOneField(primary_key=True,
                                                         serialize=False,
                                                         to='common.BPAUniqueID',
                                                         help_text=b'Bioplatforms Australia Sample ID',
                                                         verbose_name=b'BPA ID'), ),
    ]
