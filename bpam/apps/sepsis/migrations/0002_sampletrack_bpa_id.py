# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20160523_1340'),
        ('sepsis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(model_name='sampletrack',
                            name='bpa_id',
                            field=models.OneToOneField(null=True,
                                                       to='common.BPAUniqueID',
                                                       help_text=b'Bioplatforms Australia Sample ID',
                                                       verbose_name=b'BPA ID'), ),
    ]
