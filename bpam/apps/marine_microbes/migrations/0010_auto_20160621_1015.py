# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('marine_microbes', '0009_auto_20160620_1538'), ]

    operations = [
        migrations.AlterField(
            model_name='mmsample',
            name='sample_type',
            field=models.CharField(blank=True,
                                   max_length=2,
                                   null=True,
                                   verbose_name=b'Sample Type',
                                   choices=[(b'Pelagic/Open Water', b'PL'), (b'Coastal Water', b'CW'),
                                            (b'Sediment', b'SE'), (b'Seagrass', b'SG'), (b'Seaweed', b'SW'),
                                            (b'Coral', b'CO'), (b'Sponge', b'SP')]), ),
    ]
