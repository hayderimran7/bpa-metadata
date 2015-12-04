# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('gbr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmpliconSequenceFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index_number', models.IntegerField(null=True, verbose_name='Index', blank=True)),
                ('lane_number', models.IntegerField(null=True, verbose_name='Lane', blank=True)),
                ('read_number', models.IntegerField(null=True, verbose_name='Read', blank=True)),
                ('date_received_from_sequencing_facility', models.DateField(null=True, blank=True)),
                ('filename', models.CharField(max_length=300, null=True, verbose_name='File Name', blank=True)),
                ('md5', models.CharField(max_length=32, null=True, verbose_name='MD5 Checksum', blank=True)),
                ('analysed', models.NullBooleanField(default=False)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Amplicon Sequence Files',
            },
        ),
        migrations.CreateModel(
            name='AmpliconSequencingMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('sample_extraction_id', models.CharField(max_length=200, null=True, verbose_name='Sample Extraction ID', blank=True)),
                ('target', models.CharField(max_length=4, verbose_name='Type', choices=[(b'16S', b'16S'), (b'ITS', b'ITS'), (b'18S', b'18S'), (b'A16S', b'A16S')])),
                ('index', models.CharField(max_length=50, null=True, verbose_name='Index', blank=True)),
                ('pcr_1_to_10', models.CharField(blank=True, max_length=1, null=True, verbose_name='PCR 1:10', choices=[(b'P', b'Pass'), (b'F', b'Fail')])),
                ('pcr_1_to_100', models.CharField(blank=True, max_length=1, null=True, verbose_name='PCR 1:100', choices=[(b'P', b'Pass'), (b'F', b'Fail')])),
                ('pcr_neat', models.CharField(blank=True, max_length=1, null=True, verbose_name='Neat PCR', choices=[(b'P', b'Pass'), (b'F', b'Fail')])),
                ('dilution', models.CharField(blank=True, max_length=5, null=True, verbose_name='Dilution Used', choices=[(b'1:10', b'1:10'), (b'1:100', b'1:100'), (b'NEAT', b'Neat')])),
                ('sequencing_run_number', models.CharField(max_length=40, null=True, verbose_name='Sequencing run number', blank=True)),
                ('flow_cell_id', models.CharField(max_length=5, null=True, verbose_name='Flow Cell ID', blank=True)),
                ('reads', models.IntegerField(null=True, verbose_name='Number of Reads', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Sample Name', blank=True)),
                ('comments', models.TextField(null=True, verbose_name='Comments', blank=True)),
                ('analysis_software_version', models.CharField(max_length=100, null=True, verbose_name='Analysis Software Version', blank=True)),
                ('bpa_id', models.ForeignKey(related_name='gbr_amplicon_ampliconsequencingmetadata_related', verbose_name='BPA ID', to='common.BPAUniqueID')),
                ('sequencing_facility', models.ForeignKey(related_name='gbr_amplicon_ampliconsequencingmetadata', verbose_name='Sequencing Facility', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'verbose_name_plural': 'Amplicon Sequencing Metadata',
            },
        ),
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='metadata',
            field=models.ForeignKey(to='gbr_amplicon.AmpliconSequencingMetadata'),
        ),
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='sample',
            field=models.ForeignKey(to='gbr.GBRSample'),
        ),
        migrations.AddField(
            model_name='ampliconsequencefile',
            name='url_verification',
            field=models.ForeignKey(related_name='gbr_amplicon_ampliconsequencefile_related', to='common.URLVerification', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='ampliconsequencingmetadata',
            unique_together=set([('bpa_id', 'target')]),
        ),
    ]
