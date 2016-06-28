# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('common', '0001_initial'), ]

    operations = [
        migrations.AddField(model_name='bpauniqueid',
                            name='sra_id',
                            field=models.CharField(null=True,
                                                   max_length=12,
                                                   blank=True,
                                                   help_text=b'SRA ID',
                                                   unique=True,
                                                   verbose_name='SRA ID'), ),
    ]
