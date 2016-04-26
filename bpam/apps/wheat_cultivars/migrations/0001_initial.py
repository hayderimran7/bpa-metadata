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
            name='CultivarSample',
            fields=[
                ('bpa_id', models.OneToOneField(primary_key=True, serialize=False, to='common.BPAUniqueID', verbose_name='BPA ID')),
                ('name', models.CharField(max_length=200, verbose_name='Sample Name')),
                ('dna_extraction_protocol', models.TextField(null=True, verbose_name='DNA Extraction Protocol', blank=True)),
                ('requested_sequence_coverage', models.CharField(max_length=50, blank=True)),
                ('collection_date', models.DateField(null=True, verbose_name='Collection Date', blank=True)),
                ('date_sent_to_sequencing_facility', models.DateField(null=True, verbose_name='Date sent to sequencing facility', blank=True)),
                ('note', models.TextField(null=True, verbose_name='Note', blank=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data', blank=True)),
                ('sample_label', models.CharField(max_length=200, null=True, blank=True)),
                ('source_name', models.CharField(max_length=50, null=True, verbose_name='Source', blank=True)),
                ('cultivar_code', models.CharField(max_length=3, null=True, verbose_name='Code', blank=True)),
                ('characteristics', models.CharField(max_length=100, null=True, verbose_name='Characteristics', blank=True)),
                ('variety', models.CharField(max_length=100, null=True, verbose_name='Variety', blank=True)),
                ('organism_part', models.CharField(max_length=100, null=True, verbose_name='Organism Part', blank=True)),
                ('pedigree', models.TextField(null=True, verbose_name='Pedigree', blank=True)),
                ('dev_stage', models.CharField(max_length=200, null=True, verbose_name='Developmental Stage', blank=True)),
                ('yield_properties', models.CharField(max_length=200, null=True, verbose_name='Yield', blank=True)),
                ('morphology', models.CharField(max_length=200, null=True, verbose_name='Morphology', blank=True)),
                ('maturity', models.CharField(max_length=200, null=True, verbose_name='Maturity', blank=True)),
                ('pathogen_tolerance', models.CharField(max_length=200, null=True, verbose_name='Pathogen Tolerance', blank=True)),
                ('drought_tolerance', models.CharField(max_length=200, null=True, verbose_name='Drought Tolerance', blank=True)),
                ('soil_tolerance', models.CharField(max_length=200, null=True, verbose_name='Soil Tolerance', blank=True)),
                ('classification', models.CharField(max_length=200, null=True, verbose_name='Classification', blank=True)),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('contact_scientist', models.ForeignKey(related_name='wheat_cultivars_cultivarsample_sample', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('dna_source', models.ForeignKey(related_name='wheat_cultivars_cultivarsample_sample', verbose_name='DNA Source', blank=True, to='common.DNASource', null=True)),
                ('organism', models.ForeignKey(to='common.Organism')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sample',
            },
        ),
        migrations.CreateModel(
            name='CultivarSequenceFile',
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
                ('run_number', models.IntegerField(null=True, blank=True)),
                ('barcode', models.CharField(max_length=20, null=True, blank=True)),
                ('flowcell', models.CharField(max_length=20, null=True, blank=True)),
                ('casava_version', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Sequence File',
            },
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('library_type', models.CharField(max_length=2, verbose_name='Type', choices=[(b'PE', b'Paired End'), (b'SE', b'Single End'), (b'MP', b'Mate Pair'), (b'UN', b'Unknown')])),
                ('library_construction', models.CharField(max_length=200, null=True, verbose_name='Construction', blank=True)),
                ('base_pairs', models.IntegerField(null=True, verbose_name='Base Pairs', blank=True)),
                ('library_construction_protocol', models.CharField(max_length=200, verbose_name='Construction Protocol')),
                ('sequencer', models.CharField(max_length=200, verbose_name='Sequencer')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Protocol',
                'verbose_name_plural': 'Protocol',
            },
        ),
        migrations.AddField(
            model_name='cultivarsequencefile',
            name='protocol',
            field=models.ForeignKey(to='wheat_cultivars.Protocol'),
        ),
        migrations.AddField(
            model_name='cultivarsequencefile',
            name='sample',
            field=models.ForeignKey(to='wheat_cultivars.CultivarSample'),
        ),
        migrations.AddField(
            model_name='cultivarsequencefile',
            name='url_verification',
            field=models.ForeignKey(related_name='wheat_cultivars_cultivarsequencefile_related', to='common.URLVerification', null=True),
        ),
    ]
