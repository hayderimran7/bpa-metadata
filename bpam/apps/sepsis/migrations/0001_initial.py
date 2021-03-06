# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('common', '0006_auto_20160523_1340'), ]

    operations = [
        migrations.CreateModel(
            name='GenomicsMiseqFile',
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
                ('extraction', models.IntegerField(default=1, verbose_name=b'Extraction')),
                ('vendor', models.CharField(default=1, max_length=100, verbose_name=b'Vendor')),
                ('library', models.CharField(
                    help_text=b'MP or PE', max_length=20, verbose_name=b'Library')),
                ('size', models.CharField(default=1, max_length=100,
                                          verbose_name=b'Extraction Size')),
                ('flow_cell_id', models.CharField(max_length=6, verbose_name=b'Flow Cell ID')),
                ('index', models.CharField(max_length=20, verbose_name=b'Index')),
                ('runsamplenum', models.CharField(max_length=20, verbose_name=b'Sample Run Number')),
                ('read', models.CharField(max_length=3, verbose_name=b'Read')),
            ],
            options={
                'abstract': False,
            }, ),
        migrations.CreateModel(
            name='GrowthMethod',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('note', models.TextField(max_length=200, null=True,
                                          verbose_name=b'Note',
                                          blank=True)),
                ('growth_condition_temperature', models.IntegerField(help_text=b'Degrees Centigrade',
                                                                     null=True,
                                                                     verbose_name=b'Growth condition temperature',
                                                                     blank=True)),
                ('growth_condition_time', models.IntegerField(help_text=b'Hours',
                                                              null=True,
                                                              verbose_name=b'Growth condition time',
                                                              blank=True)),
                ('growth_condition_media', models.CharField(max_length=200,
                                                            null=True,
                                                            verbose_name=b'Growth condition media',
                                                            blank=True)),
            ],
            options={
                'verbose_name': 'Growth Method',
            }, ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('description', models.CharField(
                    max_length=200, null=True, verbose_name=b'Host Description',
                    blank=True)),
                ('location', models.CharField(help_text=b'State, Country',
                                              max_length=200,
                                              null=True,
                                              verbose_name=b'Host Location',
                                              blank=True)),
                ('sex', models.CharField(blank=True,
                                         max_length=1,
                                         null=True,
                                         verbose_name=b'Host Sex',
                                         choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('age', models.IntegerField(null=True, verbose_name=b'Host Age',
                                            blank=True)),
                ('dob', models.DateField(help_text=b'DD/MM/YY',
                                         null=True,
                                         verbose_name=b'Host Day of Birth',
                                         blank=True)),
                ('disease_outcome', models.TextField(null=True,
                                                     verbose_name=b'Host Disease Outcome',
                                                     blank=True)),
                ('strain_or_isolate', models.CharField(max_length=200,
                                                       unique=True,
                                                       null=True,
                                                       verbose_name=b'Strain Or Isolate',
                                                       blank=True)),
            ],
            options={
                'verbose_name': 'Host',
            }, ),
        migrations.CreateModel(
            name='MiseqGenomicsMethod',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100,
                                                                   null=True,
                                                                   verbose_name=b'Library Construction Protocol',
                                                                   blank=True)),
                ('insert_size_range', models.CharField(
                    max_length=20, null=True, verbose_name=b'Insert Size Range',
                    blank=True)),
                ('sequencer', models.CharField(
                    max_length=100, null=True, verbose_name=b'Sequencer',
                    blank=True)),
                ('analysis_software_version', models.CharField(max_length=20,
                                                               null=True,
                                                               verbose_name=b'Analysis Software Version',
                                                               blank=True)),
            ],
            options={
                'verbose_name': 'Miseq Genomics Method',
            }, ),
        migrations.CreateModel(
            name='PacBioGenomicsMethod',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100,
                                                                   null=True,
                                                                   verbose_name=b'Library Construction Protocol',
                                                                   blank=True)),
                ('insert_size_range', models.CharField(
                    max_length=20, null=True, verbose_name=b'Insert Size Range',
                    blank=True)),
                ('sequencer', models.CharField(
                    max_length=100, null=True, verbose_name=b'Sequencer',
                    blank=True)),
                ('sequencer_run_id', models.CharField(
                    max_length=20, null=True, verbose_name=b'Sequencer run ID',
                    blank=True)),
                ('smrt_cell_id', models.CharField(
                    max_length=60, null=True, verbose_name=b'SMRT Cell ID',
                    blank=True)),
                ('cell_position', models.CharField(
                    max_length=60, null=True, verbose_name=b'Cell Position',
                    blank=True)),
                ('rs_version', models.CharField(
                    max_length=20, null=True, verbose_name=b'RS Version',
                    blank=True)),
            ],
            options={
                'verbose_name': 'PacBio Genomics Method',
            }, ),
        migrations.CreateModel(
            name='ProteomicsFile',
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
                'abstract': False,
            }, ),
        migrations.CreateModel(
            name='ProteomicsMethod',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('sample_fractionation', models.IntegerField(null=True,
                                                             verbose_name=b'Sample Fractionation',
                                                             blank=True)),
                ('lc_column_type', models.CharField(
                    max_length=100, null=True, verbose_name=b'LC/column type',
                    blank=True)),
                ('gradient', models.CharField(
                    max_length=100,
                    null=True,
                    verbose_name=b'Gradient time (min)  /  % ACN (start-finish main gradient) / flow',
                    blank=True)),
                ('column', models.CharField(max_length=100,
                                            null=True,
                                            verbose_name=b'Sample on column(\xc2\xb5g) ',
                                            blank=True)),
                ('mass_spectrometer', models.CharField(
                    max_length=100, null=True, verbose_name=b'Mass Spectrometer',
                    blank=True)),
                ('aquisition_mode', models.CharField(max_length=100,
                                                     null=True,
                                                     verbose_name=b'Acquisition Mode / fragmentation',
                                                     blank=True)),
            ],
            options={
                'verbose_name': 'Proteomics Method',
            }, ),
        migrations.CreateModel(
            name='SampleTrack',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('given_to', models.CharField(help_text=b'Sample was delivered to',
                                              max_length=200,
                                              null=True,
                                              verbose_name=b'Given To',
                                              blank=True)),
                ('allocation_date', models.DateField(help_text=b'DD/MM/YY',
                                                     null=True,
                                                     verbose_name=b'Allocation Date',
                                                     blank=True)),
                ('work_order', models.CharField(
                    max_length=50, null=True, verbose_name=b'Work Order',
                    blank=True)),
                ('replicate', models.IntegerField(null=True, verbose_name=b'Replicate',
                                                  blank=True)),
                ('omics', models.CharField(max_length=50,
                                           null=True, verbose_name=b'Omics Type',
                                           blank=True)),
                ('analytical_platform', models.CharField(max_length=100,
                                                         null=True,
                                                         verbose_name=b'Analytical Platform',
                                                         blank=True)),
                ('data_generated', models.BooleanField(default=False, verbose_name=b'Data Generated')),
                ('sample_submission_date', models.DateField(help_text=b'DD/MM/YY',
                                                            null=True,
                                                            verbose_name=b'Sample Submission Date',
                                                            blank=True)),
                ('contextual_data_submission_date', models.DateField(help_text=b'DD/MM/YY',
                                                                     null=True,
                                                                     verbose_name=b'Contextual Data Submission Date',
                                                                     blank=True)),
                ('archive_ingestion_date', models.DateField(help_text=b'DD/MM/YY',
                                                            null=True,
                                                            verbose_name=b'Archive Ingestion Date',
                                                            blank=True)),
                ('curation_url', models.URLField(null=True, verbose_name=b'Curation URL',
                                                 blank=True)),
                ('dataset_url', models.URLField(null=True, verbose_name=b'Dataset URL',
                                                blank=True)),
                ('facility', models.ForeignKey(blank=True, to='common.Facility',
                                               null=True)),
            ],
            options={
                'verbose_name': 'Sample Tracking Information',
                'verbose_name_plural': 'Sample Tracking',
            }, ),
        migrations.CreateModel(
            name='SepsisSample',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('taxon_or_organism', models.CharField(
                    max_length=200, null=True, verbose_name=b'Taxon or Organism',
                    blank=True)),
                ('strain_or_isolate', models.CharField(
                    max_length=200, null=True, verbose_name=b'Strain Or Isolate',
                    blank=True)),
                ('strain_description', models.CharField(
                    max_length=300, null=True, verbose_name=b'Strain Description',
                    blank=True)),
                ('gram_stain', models.CharField(max_length=3,
                                                verbose_name=b'Gram Staining',
                                                choices=[(b'POS', b'Positive'), (b'NEG', b'Negative')])),
                ('serovar', models.CharField(max_length=100,
                                             null=True, verbose_name=b'Serovar',
                                             blank=True)),
                ('key_virulence_genes', models.CharField(max_length=100,
                                                         null=True,
                                                         verbose_name=b'Key Virulence Genes',
                                                         blank=True)),
                ('isolation_source', models.CharField(
                    max_length=100, null=True, verbose_name=b'Isolation Source',
                    blank=True)),
                ('publication_reference', models.CharField(max_length=200,
                                                           null=True,
                                                           verbose_name=b'Publication Reference',
                                                           blank=True)),
                ('contact_researcher', models.CharField(
                    max_length=200, null=True, verbose_name=b'Contact Researcher',
                    blank=True)),
                ('culture_collection_date', models.DateField(help_text=b'DD/MM/YY',
                                                             null=True,
                                                             verbose_name=b'Collection Date',
                                                             blank=True)),
                ('culture_collection_id', models.CharField(max_length=100,
                                                           null=True,
                                                           verbose_name=b'Culture Collection ID',
                                                           blank=True)),
                ('bpa_id', models.OneToOneField(verbose_name=b'BPA ID',
                                                to='common.BPAUniqueID',
                                                help_text=b'Bioplatforms Australia Sample ID')),
                ('growth_method', models.ForeignKey(related_name='samples',
                                                    blank=True,
                                                    to='sepsis.GrowthMethod',
                                                    help_text=b'Sample Growth Method',
                                                    null=True)),
                ('host', models.ForeignKey(related_name='samples',
                                           blank=True,
                                           to='sepsis.Host',
                                           help_text=b'Sample donor host',
                                           null=True)),
                ('sample_track', models.OneToOneField(related_name='sample',
                                                      null=True,
                                                      blank=True,
                                                      to='sepsis.SampleTrack',
                                                      help_text=b'Sample Tracking')),
            ],
            options={
                'verbose_name': 'Sepsis Sample',
            }, ),
        migrations.CreateModel(
            name='TranscriptomicsFile',
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
                ('sample', models.ForeignKey(to='sepsis.SepsisSample')),
                ('url_verification', models.ForeignKey(related_name='sepsis_transcriptomicsfile_related',
                                                       to='common.URLVerification',
                                                       null=True)),
            ],
            options={
                'abstract': False,
            }, ),
        migrations.CreateModel(
            name='TranscriptomicsMethod',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('library_construction_protocol', models.CharField(max_length=100,
                                                                   null=True,
                                                                   verbose_name=b'Library Construction Protocol',
                                                                   blank=True)),
                ('insert_size_range', models.CharField(
                    max_length=20, null=True, verbose_name=b'Insert Size Range',
                    blank=True)),
                ('sequencer', models.CharField(
                    max_length=100, null=True, verbose_name=b'Sequencer',
                    blank=True)),
                ('casava_version', models.CharField(
                    max_length=20, null=True, verbose_name=b'CASAVA Version',
                    blank=True)),
            ],
            options={
                'verbose_name': 'Transcriptomics Method',
            }, ),
        migrations.AddField(model_name='proteomicsfile',
                            name='sample',
                            field=models.ForeignKey(to='sepsis.SepsisSample'), ),
        migrations.AddField(model_name='proteomicsfile',
                            name='url_verification',
                            field=models.ForeignKey(related_name='sepsis_proteomicsfile_related',
                                                    to='common.URLVerification',
                                                    null=True), ),
        migrations.AddField(model_name='genomicsmiseqfile',
                            name='method',
                            field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_files',
                                                    to='sepsis.MiseqGenomicsMethod',
                                                    help_text=b'Genomics Method',
                                                    null=True), ),
        migrations.AddField(model_name='genomicsmiseqfile',
                            name='sample',
                            field=models.ForeignKey(to='sepsis.SepsisSample'), ),
        migrations.AddField(model_name='genomicsmiseqfile',
                            name='url_verification',
                            field=models.ForeignKey(related_name='sepsis_genomicsmiseqfile_related',
                                                    to='common.URLVerification',
                                                    null=True), ),
    ]
