# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Array',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('array_id', models.CharField(max_length=17, verbose_name='Array ID')),
                ('batch_number', models.IntegerField(verbose_name='Batch')),
                ('well_id', models.CharField(max_length=4, verbose_name='Well ID')),
                ('mia_id', models.CharField(max_length=200, verbose_name='MIA ID')),
                ('call_rate', models.FloatField()),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'U', b'Unknown')])),
            ],
        ),
        migrations.CreateModel(
            name='MelanomaProtocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'PE', b'Paired End'), (b'SE', b'Single End'), (b'MP', b'Mate Pair'), (b'UN', b'Unknown')])),
                ('library_construction', models.CharField(max_length=200, null=True, verbose_name='Construction', blank=True)),
                ('base_pairs', models.IntegerField(null=True, verbose_name='Base Pairs', blank=True)),
                ('library_construction_protocol', models.TextField(verbose_name='Construction Protocol')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocol',
            },
        ),
        migrations.CreateModel(
            name='MelanomaRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DNA_extraction_protocol', models.CharField(max_length=200, verbose_name='DNA Extraction Protocol', blank=True)),
                ('passage_number', models.IntegerField(null=True, verbose_name='Passage Number', blank=True)),
                ('run_number', models.IntegerField(null=True, blank=True)),
                ('flow_cell_id', models.CharField(max_length=10, verbose_name='Flow Cell ID', blank=True)),
                ('array_analysis_facility', models.ForeignKey(related_name='+', verbose_name='Array Analysis', blank=True, to='common.Facility', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Run',
            },
        ),
        migrations.CreateModel(
            name='MelanomaSample',
            fields=[
                ('bpa_id', models.OneToOneField(primary_key=True, serialize=False, to='common.BPAUniqueID', verbose_name='BPA ID')),
                ('name', models.CharField(max_length=200, verbose_name='Sample Name')),
                ('dna_extraction_protocol', models.TextField(null=True, verbose_name='DNA Extraction Protocol', blank=True)),
                ('requested_sequence_coverage', models.CharField(max_length=50, blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('date_sent_to_sequencing_facility', models.DateField(null=True, verbose_name='Date sent to sequencing facility', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('passage_number', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'U', b'Unknown')])),
                ('histological_subtype', models.CharField(max_length=50, null=True)),
                ('contact_scientist', models.ForeignKey(related_name='melanoma_melanomasample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('dna_source', models.ForeignKey(related_name='melanoma_melanomasample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True)),
                ('organism', models.ForeignKey(to='common.Organism')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample',
            },
        ),
        migrations.CreateModel(
            name='MelanomaSequenceFile',
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
                ('run', models.ForeignKey(to='melanoma.MelanomaRun')),
                ('sample', models.ForeignKey(to='melanoma.MelanomaSample')),
                ('url_verification', models.ForeignKey(related_name='melanoma_melanomasequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sequence File',
            },
        ),
        migrations.CreateModel(
            name='TumorStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='melanomasample',
            name='tumor_stage',
            field=models.ForeignKey(to='melanoma.TumorStage', null=True),
        ),
        migrations.AddField(
            model_name='melanomarun',
            name='sample',
            field=models.ForeignKey(to='melanoma.MelanomaSample'),
        ),
        migrations.AddField(
            model_name='melanomarun',
            name='sequencer',
            field=models.ForeignKey(blank=True, to='common.Sequencer', null=True),
        ),
        migrations.AddField(
            model_name='melanomarun',
            name='sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Sequencing', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='melanomarun',
            name='whole_genome_sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Whole Genome', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='melanomaprotocol',
            name='run',
            field=models.OneToOneField(null=True, blank=True, to='melanoma.MelanomaRun'),
        ),
        migrations.AddField(
            model_name='array',
            name='bpa_id',
            field=models.ForeignKey(verbose_name='BPA ID', to='common.BPAUniqueID'),
        ),
        migrations.AlterUniqueTogether(
            name='melanomaprotocol',
            unique_together=set([('library_type', 'base_pairs', 'library_construction_protocol')]),
        ),
    ]
