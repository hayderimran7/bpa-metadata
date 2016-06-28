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
            name='Sample454',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('debug_note', models.TextField(null=True, verbose_name='Original Data',
                                                blank=True)),
                ('sample_id', models.CharField(
                    max_length=100, null=True, verbose_name='Sample ID',
                    blank=True)),
                ('aurora_purified', models.BooleanField(default=False, verbose_name='Aurora Purified')),
                ('dna_storage_nunc_plate', models.CharField(
                    default=b'', max_length=12,
                    null=True, verbose_name='Nunc Plate',
                    blank=True)),
                ('dna_storage_nunc_tube', models.CharField(
                    default=b'', max_length=12,
                    null=True, verbose_name='Nunc Tube',
                    blank=True)),
                ('dna_storage_nunc_well_location', models.CharField(
                    max_length=30, null=True, verbose_name='Well Location',
                    blank=True)),
                ('agrf_batch_number', models.CharField(
                    max_length=15, null=True, verbose_name='AGRF Batch Number',
                    blank=True)),
                ('date_received', models.DateField(null=True, blank=True)),
                ('adelaide_extraction_sample_weight', models.CharField(max_length=30,
                                                                       null=True,
                                                                       verbose_name='Extraction Sample Weight (mg)',
                                                                       blank=True)),
                ('adelaide_fluorimetry', models.FloatField(null=True,
                                                           verbose_name='Fluorimetry ng/uL gDNA',
                                                           blank=True)),
                ('adelaide_pcr_inhibition', models.CharField(
                    max_length=2,
                    verbose_name='PCR Inhibition (neat plus spike) 16S (V3-V8)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('adelaide_pcr1', models.CharField(
                    max_length=2,
                    verbose_name='PCR1 (neat) 16S (V3-V8)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('adelaide_pcr2', models.CharField(
                    max_length=2,
                    verbose_name='PCR2 (1:100) 16S (V3-V8)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('adelaide_date_shipped_to_agrf_454', models.DateField(null=True,
                                                                       verbose_name='DNA shipped to AGRF (454)',
                                                                       blank=True)),
                ('adelaide_date_shipped_to_agrf_miseq', models.DateField(null=True,
                                                                         verbose_name='DNA shipped to AGRF (MiSeq)',
                                                                         blank=True)),
                ('adelaide_date_shipped_to_ramacciotti', models.DateField(null=True,
                                                                          verbose_name='DNA shipped to Ramaciotti',
                                                                          blank=True)),
                ('brisbane_16s_mid', models.CharField(
                    max_length=7, null=True, verbose_name='16S MID',
                    blank=True)),
                ('brisbane_its_mid', models.CharField(
                    max_length=7, null=True, verbose_name='ITS MID',
                    blank=True)),
                ('brisbane_16s_pcr1', models.CharField(
                    max_length=2,
                    verbose_name='16S (V1-V3) PCR1 (neat)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_16s_pcr2', models.CharField(
                    max_length=2,
                    verbose_name='16S (V1-V3) PCR2 (1:10)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_16s_pcr3', models.CharField(
                    max_length=2,
                    verbose_name='16S (V1-V3) PCR3 (fusion-primer)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_its_pcr1_neat', models.CharField(
                    max_length=2,
                    verbose_name='ITS PCR1 (neat)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_its_pcr2_1_10', models.CharField(
                    max_length=2,
                    verbose_name='ITS PCR1 (1:10)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_its_pcr3_fusion', models.CharField(
                    max_length=2,
                    verbose_name='ITS PCR3 (fusion-primer)',
                    choices=[(b'P', b'Pass'), (b'F', b'Failed'), (b'NP', b'Not Performed'), (b'U', b'Unknown'), (
                        b'R', b'Repeat')])),
                ('brisbane_fluorimetry_16s', models.FloatField(null=True,
                                                               verbose_name='Fluorimetry ng/uL 16S',
                                                               blank=True)),
                ('brisbane_fluorimetry_its', models.FloatField(null=True,
                                                               verbose_name='Fluorimetry ng/uL ITS',
                                                               blank=True)),
                ('brisbane_16s_qpcr', models.FloatField(null=True, verbose_name='16S qPCR',
                                                        blank=True)),
                ('brisbane_its_qpcr', models.FloatField(null=True, verbose_name='ITS qPCR',
                                                        blank=True)),
                ('brisbane_i6s_pooled', models.NullBooleanField(verbose_name='16S pooled')),
                ('brisbane_its_pooled', models.NullBooleanField(verbose_name='ITS pooled')),
                ('brisbane_16s_reads', models.IntegerField(null=True,
                                                           verbose_name='16S >3000 reads - Trim Back 150bp',
                                                           blank=True)),
                ('brisbane_its_reads', models.IntegerField(null=True,
                                                           verbose_name='ITS >3000 reads - Trim Back 150bp Run1',
                                                           blank=True)),
                ('note', models.TextField(null=True, blank=True)),
                ('bpa_id', models.OneToOneField(verbose_name='BPA ID', to='common.BPAUniqueID')),
                ('submitter', models.ForeignKey(verbose_name='Submitter',
                                                blank=True,
                                                to=settings.AUTH_USER_MODEL,
                                                null=True)),
            ],
            options={
                'verbose_name_plural': 'Sample 454',
            }, ),
    ]
