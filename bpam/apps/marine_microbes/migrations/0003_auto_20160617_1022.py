# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_site'),
        ('marine_microbes', '0002_auto_20160615_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetagenomiSequenceFile',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('index_number', models.IntegerField(null=True, verbose_name=b'Index Number',
                                                     blank=True)),
                ('lane_number', models.IntegerField(null=True, verbose_name=b'Lane Number',
                                                    blank=True)),
                ('read_number', models.IntegerField(null=True, verbose_name=b'Read Number',
                                                    blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(
                    max_length=300, null=True, verbose_name=b'File Name',
                    blank=True)),
                ('md5', models.CharField(max_length=32,
                                         null=True, verbose_name=b'MD5 Checksum',
                                         blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Metagenomics Sequence Files',
            }, ),
        migrations.CreateModel(name='MMSample',
                               fields=[
                                   ('bpa_id', models.OneToOneField(primary_key=True,
                                                                   serialize=False,
                                                                   to='common.BPAUniqueID',
                                                                   help_text=b'Bioplatforms Australia Sample ID',
                                                                   verbose_name=b'BPA ID')),
                               ],
                               options={
                                   'verbose_name': 'Sepsis Sample',
                               }, ),
        migrations.AddField(model_name='metagenomisequencefile',
                            name='sample',
                            field=models.ForeignKey(to='marine_microbes.MMSample'), ),
        migrations.AddField(model_name='metagenomisequencefile',
                            name='url_verification',
                            field=models.ForeignKey(related_name='marine_microbes_metagenomisequencefile_related',
                                                    to='common.URLVerification',
                                                    null=True), ),
    ]
