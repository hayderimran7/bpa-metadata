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
            name='WheatPathogenTranscriptProtocol',
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
            name='WheatPathogenTranscriptRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('DNA_extraction_protocol', models.CharField(max_length=200, verbose_name='DNA Extraction Protocol', blank=True)),
                ('passage_number', models.IntegerField(null=True, verbose_name='Passage Number', blank=True)),
                ('run_number', models.IntegerField(null=True, blank=True)),
                ('flow_cell_id', models.CharField(max_length=10, verbose_name='Flow Cell ID', blank=True)),
                ('array_analysis_facility', models.ForeignKey(related_name='+', verbose_name='Array Analysis', blank=True, to='common.Facility', null=True)),
                ('protocol', models.ForeignKey(blank=True, to='wheat_pathogens_transcript.WheatPathogenTranscriptProtocol', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Run',
            },
        ),
        migrations.CreateModel(
            name='WheatPathogenTranscriptSample',
            fields=[
                ('bpa_id', models.OneToOneField(primary_key=True, serialize=False, to='common.BPAUniqueID', verbose_name='BPA ID')),
                ('name', models.CharField(max_length=200, verbose_name='Sample Name')),
                ('dna_extraction_protocol', models.TextField(null=True, verbose_name='DNA Extraction Protocol', blank=True)),
                ('requested_sequence_coverage', models.CharField(max_length=50, blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('date_sent_to_sequencing_facility', models.DateField(null=True, verbose_name='Date sent to sequencing facility', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('project', models.CharField(max_length=200, null=True, blank=True)),
                ('sample_label', models.CharField(max_length=200, null=True, blank=True)),
                ('index', models.CharField(max_length=6, null=True, blank=True)),
                ('institution', models.CharField(max_length=200, null=True, blank=True)),
                ('species', models.CharField(max_length=100, null=True, blank=True)),
                ('sample_type', models.CharField(max_length=20, null=True, blank=True)),
                ('extraction_method', models.TextField(null=True, blank=True)),
                ('growth_protocol', models.TextField(null=True, blank=True)),
                ('treatment_protocol', models.TextField(null=True, blank=True)),
                ('experimental_design', models.TextField(null=True, blank=True)),
                ('contact_scientist', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('dna_source', models.ForeignKey(verbose_name='DNA Source', blank=True, to='common.DNASource', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample',
            },
        ),
        migrations.CreateModel(
            name='WheatPathogenTranscriptSequenceFile',
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
                ('file_size', models.CharField(max_length=10, null=True, blank=True)),
                ('run', models.ForeignKey(to='wheat_pathogens_transcript.WheatPathogenTranscriptRun')),
                ('sample', models.ForeignKey(to='wheat_pathogens_transcript.WheatPathogenTranscriptSample')),
                ('url_verification', models.ForeignKey(related_name='wheat_pathogens_transcript_wheatpathogentranscriptsequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sequence File',
            },
        ),
        migrations.AddField(
            model_name='wheatpathogentranscriptrun',
            name='sample',
            field=models.ForeignKey(to='wheat_pathogens_transcript.WheatPathogenTranscriptSample'),
        ),
        migrations.AddField(
            model_name='wheatpathogentranscriptrun',
            name='sequencer',
            field=models.ForeignKey(blank=True, to='common.Sequencer', null=True),
        ),
        migrations.AddField(
            model_name='wheatpathogentranscriptrun',
            name='sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Sequencing', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='wheatpathogentranscriptrun',
            name='whole_genome_sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Whole Genome', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='wheatpathogentranscriptprotocol',
            name='run',
            field=models.ForeignKey(blank=True, to='wheat_pathogens_transcript.WheatPathogenTranscriptRun', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='wheatpathogentranscriptprotocol',
            unique_together=set([('library_type', 'base_pairs', 'library_construction_protocol')]),
        ),
    ]
