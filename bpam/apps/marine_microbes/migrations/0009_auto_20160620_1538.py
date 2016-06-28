# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_site'),
        ('marine_microbes', '0008_auto_20160617_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmsample',
            name='collection_date',
            field=models.DateTimeField(null=True, verbose_name=b'Sample Collection Date',
                                       blank=True), ),
        migrations.AddField(
            model_name='mmsample',
            name='depth',
            field=models.IntegerField(null=True, verbose_name=b'Depth', blank=True), ),
        migrations.AddField(
            model_name='mmsample',
            name='sample_type',
            field=models.CharField(blank=True,
                                   max_length=2,
                                   null=True,
                                   verbose_name=b'Sample Type',
                                   choices=[(b'Open Water', b'OW'), (b'Coastal Water', b'CW'), (b'Sediment', b'SE'),
                                            (b'Seagrass', b'SG'), (b'Seaweed', b'SW'), (b'Coral', b'CO'),
                                            (b'Sponge', b'SP')]), ),
        migrations.AddField(model_name='mmsample',
                            name='site',
                            field=models.ForeignKey(to='common.Site', null=True), ),
    ]
