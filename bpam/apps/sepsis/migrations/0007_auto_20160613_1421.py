# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('sepsis', '0006_genomicspacbiofile'), ]

    operations = [
        migrations.AlterField(model_name='genomicsmiseqfile',
                              name='sample',
                              field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_files',
                                                      to='sepsis.SepsisSample'), ),
        migrations.AlterField(model_name='genomicspacbiofile',
                              name='sample',
                              field=models.ForeignKey(related_name='sepsis_genomicspacbiofile_files',
                                                      to='sepsis.SepsisSample'), ),
        migrations.AlterField(model_name='proteomicsfile',
                              name='sample',
                              field=models.ForeignKey(related_name='sepsis_proteomicsfile_files',
                                                      to='sepsis.SepsisSample'), ),
        migrations.AlterField(model_name='transcriptomicsfile',
                              name='sample',
                              field=models.ForeignKey(related_name='sepsis_transcriptomicsfile_files',
                                                      to='sepsis.SepsisSample'), ),
    ]
