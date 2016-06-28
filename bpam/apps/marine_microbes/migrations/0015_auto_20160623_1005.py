# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('marine_microbes', '0014_auto_20160622_1438'), ]

    operations = [
        migrations.AddField(model_name='ampliconsequencefile',
                            name='analysis_software_version',
                            field=models.CharField(max_length=100,
                                                   null=True,
                                                   verbose_name=b'Analysis Software Version',
                                                   blank=True), ),
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='dilution',
            field=models.CharField(blank=True,
                                   max_length=5,
                                   null=True,
                                   verbose_name=b'Dilution Used',
                                   choices=[(b'1:10', b'1:10'), (b'1:100', b'1:100'), (b'NEAT', b'Neat')]), ),
        migrations.AddField(model_name='ampliconsequencefile',
                            name='pcr_1_to_10',
                            field=models.CharField(blank=True,
                                                   max_length=1,
                                                   null=True,
                                                   verbose_name=b'PCR 1:10',
                                                   choices=[(b'P', b'Pass'), (b'F', b'Fail')]), ),
        migrations.AddField(model_name='ampliconsequencefile',
                            name='pcr_1_to_100',
                            field=models.CharField(blank=True,
                                                   max_length=1,
                                                   null=True,
                                                   verbose_name=b'PCR 1:100',
                                                   choices=[(b'P', b'Pass'), (b'F', b'Fail')]), ),
        migrations.AddField(model_name='ampliconsequencefile',
                            name='pcr_neat',
                            field=models.CharField(blank=True,
                                                   max_length=1,
                                                   null=True,
                                                   verbose_name=b'Neat PCR',
                                                   choices=[(b'P', b'Pass'), (b'F', b'Fail')]), ),
    ]
