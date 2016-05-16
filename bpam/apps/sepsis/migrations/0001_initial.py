# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_auto_20160427_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenomicsFile',
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
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=200, null=True, verbose_name=b'Note', blank=True)),
                ('growth_condition_temperature', models.IntegerField(help_text=b'Degrees Centigrade', null=True, verbose_name=b'Growth condition temperature', blank=True)),
                ('growth_condition_time', models.IntegerField(help_text=b'Hours', null=True, verbose_name=b'Growth condition time', blank=True)),
                ('growth_condition_media', models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True)),
                ('library_construction_protocol', models.CharField(max_length=100, null=True, verbose_name=b'Library Construction Protocol', blank=True)),
                ('insert_size_range', models.CharField(max_length=20, null=True, verbose_name=b'Insert Size Range', blank=True)),
                ('sequencer', models.CharField(max_length=100, null=True, verbose_name=b'Sequencer', blank=True)),
                ('sequencer_run_id', models.CharField(max_length=20, null=True, verbose_name=b'Sequencer run ID', blank=True)),
                ('smrt_cell_id', models.CharField(max_length=60, null=True, verbose_name=b'SMRT Cell ID', blank=True)),
                ('cell_position', models.CharField(max_length=60, null=True, verbose_name=b'Cell Position', blank=True)),
                ('rs_version', models.CharField(max_length=20, null=True, verbose_name=b'RS Version', blank=True)),
            ],
            options={
                'verbose_name': 'Genomics Method',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name=b'Host Description', blank=True)),
                ('location', models.CharField(help_text=b'State, Country', max_length=200, null=True, verbose_name=b'Host Location', blank=True)),
                ('sex', models.CharField(blank=True, max_length=1, null=True, verbose_name=b'Host Sex', choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('age', models.IntegerField(null=True, verbose_name=b'Host Age', blank=True)),
                ('dob', models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Host Day of Birth', blank=True)),
                ('disease_outcome', models.TextField(null=True, verbose_name=b'Host Disease Outcome', blank=True)),
            ],
            options={
                'verbose_name': 'Host',
            },
        ),
        migrations.CreateModel(
            name='ProteomicsFile',
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
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProteomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=200, null=True, verbose_name=b'Note', blank=True)),
                ('growth_condition_temperature', models.IntegerField(help_text=b'Degrees Centigrade', null=True, verbose_name=b'Growth condition temperature', blank=True)),
                ('growth_condition_time', models.IntegerField(help_text=b'Hours', null=True, verbose_name=b'Growth condition time', blank=True)),
                ('growth_condition_media', models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True)),
                ('sample_fractionation', models.IntegerField(null=True, verbose_name=b'Sample Fractionation', blank=True)),
                ('lc_column_type', models.CharField(max_length=100, null=True, verbose_name=b'LC/column type', blank=True)),
                ('gradient', models.CharField(max_length=100, null=True, verbose_name=b'Gradient time (min)  /  % ACN (start-finish main gradient) / flow', blank=True)),
                ('column', models.CharField(max_length=100, null=True, verbose_name=b'Sample on column(\xc2\xb5g) ', blank=True)),
                ('mass_spectrometer', models.CharField(max_length=100, null=True, verbose_name=b'Mass Spectrometer', blank=True)),
                ('aquisition_mode', models.CharField(max_length=100, null=True, verbose_name=b'Acquisition Mode / fragmentation', blank=True)),
            ],
            options={
                'verbose_name': 'Proteomics Method',
            },
        ),
        migrations.CreateModel(
            name='SepsisSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taxon_or_organism', models.TextField(max_length=200, null=True, verbose_name=b'Taxon or Organism', blank=True)),
                ('strain_or_isolate', models.TextField(max_length=200, null=True, verbose_name=b'Strain Or Isolate', blank=True)),
                ('strain_description', models.TextField(max_length=300, null=True, verbose_name=b'Strain Description', blank=True)),
                ('gram_stain', models.CharField(max_length=3, verbose_name=b'Gram Staining', choices=[(b'POS', b'Positive'), (b'NEG', b'Negative')])),
                ('serovar', models.CharField(max_length=30, null=True, verbose_name=b'Serovar', blank=True)),
                ('key_virulence_genes', models.CharField(max_length=100, null=True, verbose_name=b'Key Virulence Genes', blank=True)),
                ('isolation_source', models.CharField(max_length=100, null=True, verbose_name=b'Isolation Source', blank=True)),
                ('publication_reference', models.CharField(max_length=200, null=True, verbose_name=b'Publication Reference', blank=True)),
                ('contact_researcher', models.CharField(max_length=200, null=True, verbose_name=b'Contact Researcher', blank=True)),
                ('collection_date', models.DateField(help_text=b'DD/MM/YY', null=True, verbose_name=b'Collection Date', blank=True)),
                ('culture_collection_id', models.CharField(max_length=100, null=True, verbose_name=b'Culture Collection ID', blank=True)),
                ('bpa_id', models.OneToOneField(verbose_name=b'BPA ID', to='common.BPAUniqueID')),
                ('host', models.ForeignKey(related_name='sepsis_sepsissample_sample', blank=True, to='sepsis.Host', null=True)),
            ],
            options={
                'verbose_name': 'Sepsis Sample',
            },
        ),
        migrations.CreateModel(
            name='TranscriptomicsFile',
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
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TranscriptomicsMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=200, null=True, verbose_name=b'Note', blank=True)),
                ('growth_condition_temperature', models.IntegerField(help_text=b'Degrees Centigrade', null=True, verbose_name=b'Growth condition temperature', blank=True)),
                ('growth_condition_time', models.IntegerField(help_text=b'Hours', null=True, verbose_name=b'Growth condition time', blank=True)),
                ('growth_condition_media', models.CharField(max_length=200, null=True, verbose_name=b'Growth condition media', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Growth Method',
            },
        ),
        migrations.AddField(
            model_name='transcriptomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_transcriptomicsfile_transcriptomicsfile', to='sepsis.TranscriptomicsMethod'),
        ),
        migrations.AddField(
            model_name='transcriptomicsfile',
            name='sample',
            field=models.ForeignKey(to='sepsis.SepsisSample'),
        ),
        migrations.AddField(
            model_name='transcriptomicsfile',
            name='url_verification',
            field=models.ForeignKey(related_name='sepsis_transcriptomicsfile_related', to='common.URLVerification', null=True),
        ),
        migrations.AddField(
            model_name='proteomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_proteomicsfile_proteomicsfile', to='sepsis.ProteomicsMethod'),
        ),
        migrations.AddField(
            model_name='proteomicsfile',
            name='sample',
            field=models.ForeignKey(to='sepsis.SepsisSample'),
        ),
        migrations.AddField(
            model_name='proteomicsfile',
            name='url_verification',
            field=models.ForeignKey(related_name='sepsis_proteomicsfile_related', to='common.URLVerification', null=True),
        ),
        migrations.AddField(
            model_name='genomicsfile',
            name='method',
            field=models.ForeignKey(related_name='sepsis_genomicsfile_genomicsfile', to='sepsis.GenomicsMethod'),
        ),
        migrations.AddField(
            model_name='genomicsfile',
            name='sample',
            field=models.ForeignKey(to='sepsis.SepsisSample'),
        ),
        migrations.AddField(
            model_name='genomicsfile',
            name='url_verification',
            field=models.ForeignKey(related_name='sepsis_genomicsfile_related', to='common.URLVerification', null=True),
        ),
    ]
