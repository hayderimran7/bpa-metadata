# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('wheat_pathogens', '0001_initial'), ]

    operations = [
        migrations.AlterField(model_name='pathogensequencefile',
                              name='index_number',
                              field=models.IntegerField(null=True, verbose_name=b'Index Number',
                                                        blank=True), ),
        migrations.AlterField(model_name='pathogensequencefile',
                              name='lane_number',
                              field=models.IntegerField(null=True, verbose_name=b'Lane Number',
                                                        blank=True), ),
        migrations.AlterField(model_name='pathogensequencefile',
                              name='read_number',
                              field=models.IntegerField(null=True, verbose_name=b'Read Number',
                                                        blank=True), ),
    ]
