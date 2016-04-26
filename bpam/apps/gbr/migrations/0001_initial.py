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
            name='CollectionEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('water_temp', models.FloatField(null=True, verbose_name='Water Temperature', blank=True)),
                ('water_ph', models.FloatField(null=True, verbose_name='Water pH', blank=True)),
                ('depth', models.CharField(max_length=20, null=True, verbose_name='Water Depth', blank=True)),
                ('note', models.TextField(blank=True)),
                ('collector', models.ForeignKey(related_name='collector', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(max_length=100, null=True, verbose_name='Site Name', blank=True)),
                ('lat', models.FloatField(help_text='Degree decimal', verbose_name='Latitude')),
                ('lon', models.FloatField(help_text='Degree decimal', verbose_name='Longitude')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Coral Collection Sites',
            },
        ),
        migrations.CreateModel(
            name='GBRProtocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'PE', b'Paired End'), (b'SE', b'Single End'), (b'MP', b'Mate Pair'), (b'UN', b'Unknown')])),
                ('library_construction', models.CharField(max_length=200, null=True, verbose_name='Construction', blank=True)),
                ('base_pairs', models.IntegerField(null=True, verbose_name='Base Pairs', blank=True)),
                ('library_construction_protocol', models.TextField(verbose_name='Construction Protocol')),
                ('note', models.TextField(blank=True)),
                ('base_pairs_string', models.TextField(null=True, verbose_name='Base Pairs', blank=True)),
            ],
            options={
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocol',
            },
        ),
        migrations.CreateModel(
            name='GBRRun',
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
            name='GBRSample',
            fields=[
                ('bpa_id', models.OneToOneField(primary_key=True, serialize=False, to='common.BPAUniqueID', verbose_name='BPA ID')),
                ('name', models.CharField(max_length=200, verbose_name='Sample Name')),
                ('dna_extraction_protocol', models.TextField(null=True, verbose_name='DNA Extraction Protocol', blank=True)),
                ('requested_sequence_coverage', models.CharField(max_length=50, blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('date_sent_to_sequencing_facility', models.DateField(null=True, verbose_name='Date sent to sequencing facility', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('dataset', models.CharField(max_length=100, null=True, verbose_name='Data Set', blank=True)),
                ('sequencing_notes', models.TextField(null=True, verbose_name='Sequencing Notes', blank=True)),
                ('dna_rna_concentration', models.FloatField(null=True, verbose_name='DNA/RNA Concentration', blank=True)),
                ('total_dna_rna_shipped', models.FloatField(null=True, verbose_name='Total DNA/RNA Shipped', blank=True)),
                ('comments_by_facility', models.TextField(null=True, verbose_name='Facility Comments', blank=True)),
                ('sequencing_data_eta', models.DateField(null=True, verbose_name='Sequence ETA', blank=True)),
                ('date_sequenced', models.DateField(null=True, verbose_name='Date Sequenced', blank=True)),
                ('requested_read_length', models.IntegerField(null=True, verbose_name='Requested Read Length', blank=True)),
                ('collection_event', models.ForeignKey(to='gbr.CollectionEvent', null=True)),
                ('contact_bioinformatician', models.ForeignKey(related_name='bioinformatician', verbose_name='Contact Bioinformatician', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('contact_scientist', models.ForeignKey(related_name='gbr_gbrsample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('dna_source', models.ForeignKey(related_name='gbr_gbrsample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True)),
                ('organism', models.ForeignKey(to='common.Organism', null=True)),
                ('protocol', models.ForeignKey(to='gbr.GBRProtocol', null=True)),
                ('sequencing_facility', models.ForeignKey(to='common.Facility', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample',
            },
        ),
        migrations.CreateModel(
            name='GBRSequenceFile',
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
                ('run', models.ForeignKey(to='gbr.GBRRun', null=True)),
                ('sample', models.ForeignKey(to='gbr.GBRSample')),
                ('url_verification', models.ForeignKey(related_name='gbr_gbrsequencefile_related', to='common.URLVerification', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sequence File',
            },
        ),
        migrations.AddField(
            model_name='gbrrun',
            name='sample',
            field=models.ForeignKey(to='gbr.GBRSample'),
        ),
        migrations.AddField(
            model_name='gbrrun',
            name='sequencer',
            field=models.ForeignKey(blank=True, to='common.Sequencer', null=True),
        ),
        migrations.AddField(
            model_name='gbrrun',
            name='sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Sequencing', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='gbrrun',
            name='whole_genome_sequencing_facility',
            field=models.ForeignKey(related_name='+', verbose_name='Whole Genome', blank=True, to='common.Facility', null=True),
        ),
        migrations.AddField(
            model_name='gbrprotocol',
            name='run',
            field=models.ForeignKey(to='gbr.GBRRun', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='collectionsite',
            unique_together=set([('lat', 'lon')]),
        ),
        migrations.AddField(
            model_name='collectionevent',
            name='site',
            field=models.ForeignKey(to='gbr.CollectionSite', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='gbrprotocol',
            unique_together=set([('library_type', 'base_pairs_string', 'library_construction_protocol')]),
        ),
    ]
