# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('marine_microbes', '0010_auto_20160621_1015'), ]

    operations = [
        migrations.AlterField(
            model_name='mmsample',
            name='sample_type',
            field=models.CharField(blank=True,
                                   max_length=2,
                                   null=True,
                                   verbose_name=b'Sample Type',
                                   choices=[(b'PL', b'Pelagic/Open Water'), (b'CW', b'Coastal Water'),
                                            (b'SE', b'Sediment'), (b'SG', b'Seagrass'), (b'SW', b'Seaweed'),
                                            (b'CO', b'Coral'), (b'SP', b'Sponge')]), ),
    ]
