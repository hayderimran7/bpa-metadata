# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'SoilTexture'
        db.create_table(u'BASE_soiltexture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('texture', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'BASE', ['SoilTexture'])

        # Adding model 'SoilColour'
        db.create_table(u'BASE_soilcolour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('colour', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'BASE', ['SoilColour'])

        # Adding model 'PCRPrimer'
        db.create_table(u'BASE_pcrprimer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['PCRPrimer'])

        # Adding model 'LandUse'
        db.create_table(u'BASE_landuse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classification', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['LandUse'])

        # Adding model 'GeneralEcologicalZone'
        db.create_table(u'BASE_generalecologicalzone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['GeneralEcologicalZone'])

        # Adding model 'BroadVegetationType'
        db.create_table(u'BASE_broadvegetationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vegetation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['BroadVegetationType'])

        # Adding model 'TillageType'
        db.create_table(u'BASE_tillagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tillage', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'BASE', ['TillageType'])

        # Adding model 'HorizonClassification'
        db.create_table(u'BASE_horizonclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('horizon', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'BASE', ['HorizonClassification'])

        # Adding model 'SoilClassification'
        db.create_table(u'BASE_soilclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('authority', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['SoilClassification'])

        # Adding model 'DrainageClassification'
        db.create_table(u'BASE_drainageclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drainage', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['DrainageClassification'])

        # Adding model 'ProfilePosition'
        db.create_table(u'BASE_profileposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'BASE', ['ProfilePosition'])

        # Adding model 'TargetGene'
        db.create_table(u'BASE_targetgene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['TargetGene'])

        # Adding model 'TargetTaxon'
        db.create_table(u'BASE_targettaxon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'BASE', ['TargetTaxon'])

        # Adding model 'SiteOwner'
        db.create_table(u'BASE_siteowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'BASE', ['SiteOwner'])

        # Adding model 'CollectionSiteHistory'
        db.create_table(u'BASE_collectionsitehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('current_vegetation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('previous_land_use',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='previous', to=orm['BASE.LandUse'])),
            ('current_land_use',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='current', to=orm['BASE.LandUse'])),
            ('crop_rotation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tillage', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('environment_event', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'BASE', ['CollectionSiteHistory'])

        # Adding model 'CollectionSite'
        db.create_table(u'BASE_collectionsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('horizon', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('plot_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('collection_depth', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('slope_gradient', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('slope_aspect', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('profile_position', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('drainage_classification', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('australian_classification_soil_type',
             self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('history',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BASE.CollectionSiteHistory'], null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BASE.SiteOwner'], null=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'BASE', ['CollectionSite'])

        # Adding M2M table for field positions on 'CollectionSite'
        m2m_table_name = db.shorten_name(u'BASE_collectionsite_positions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('collectionsite', models.ForeignKey(orm[u'BASE.collectionsite'], null=False)),
            ('gpsposition', models.ForeignKey(orm[u'geo.gpsposition'], null=False))
        ))
        db.create_unique(m2m_table_name, ['collectionsite_id', 'gpsposition_id'])

        # Adding model 'SoilMetagenomicsSample'
        db.create_table(u'BASE_soilmetagenomicssample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bpa_id',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.BPAUniqueID'], unique=True)),
            ('contact_scientist',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bpaauth.BPAUser'], null=True, blank=True)),
            ('dna_source',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.DNASource'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dna_extraction_protocol',
             self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('requested_sequence_coverage', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('collection_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_sent_to_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('collection_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BASE.CollectionSite'])),
        ))
        db.send_create_signal(u'BASE', ['SoilMetagenomicsSample'])

        # Adding model 'SequenceConstruct'
        db.create_table(u'BASE_sequenceconstruct', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('adapter_sequence', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('barcode_sequence', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('forward_primer', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('primer_sequence', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('target_region', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('sequence', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reverse_primer', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'BASE', ['SequenceConstruct'])

        # Adding model 'ChemicalAnalysis'
        db.create_table(u'BASE_chemicalanalysis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bpa_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.BPAUniqueID'])),
            ('lab_name_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('colour', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('gravel', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('texture', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('ammonium_nitrogen', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('nitrate_nitrogen', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('phosphorus_colwell', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('potassium_colwell', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sulphur_colwell', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('organic_carbon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('conductivity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('cacl2_ph', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('h20_ph', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dtpa_copper', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dtpa_iron', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dtpa_manganese', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('dtpa_zinc', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exc_aluminium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exc_calcium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exc_magnesium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exc_potassium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('exc_sodium', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('boron_hot_cacl2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('clay', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('course_sand', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('fine_sand', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sand', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('silt', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['ChemicalAnalysis'])

        # Adding model 'SoilSampleDNA'
        db.create_table(u'BASE_soilsampledna', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('submitter', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dna_conc', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('protocol_ref', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('library_selection', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('library_layout', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('target_taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BASE.TargetTaxon'])),
            ('target_gene',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='target', to=orm['BASE.TargetGene'])),
            ('target_subfragment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subfragment',
                                                                                         to=orm['BASE.TargetGene'])),
            ('pcr_primer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['BASE.PCRPrimer'])),
            ('pcr_primer_db_ref', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('forward_primer_sequence',
             self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('reverse_primer_sequence',
             self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pcr_reaction', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('barcode_label', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('barcode_sequence', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('performer', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            (
            'labeled_extract_name', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['SoilSampleDNA'])

        # Adding model 'Sample454'
        db.create_table(u'BASE_sample454', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bpa_id',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.BPAUniqueID'], unique=True)),
            ('sample_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('aurora_purified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dna_storage_nunc_plate',
             self.gf('django.db.models.fields.CharField')(default='', max_length=12, null=True, blank=True)),
            ('dna_storage_nunc_tube',
             self.gf('django.db.models.fields.CharField')(default='', max_length=12, null=True, blank=True)),
            ('dna_storage_nunc_well_location',
             self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('agrf_batch_number', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('submitter',
             self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='454_submitter', null=True,
                                                                   to=orm['bpaauth.BPAUser'])),
            ('date_received', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('adelaide_extraction_sample_weight',
             self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('adelaide_fluorimetry', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('adelaide_pcr_inhibition', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('adelaide_pcr1', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('adelaide_pcr2', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('adelaide_date_shipped_to_agrf_454', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            (
            'adelaide_date_shipped_to_agrf_miseq', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('adelaide_date_shipped_to_ramacciotti',
             self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('brisbane_16s_mid', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('brisbane_its_mid', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('brisbane_16s_pcr1', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_16s_pcr2', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_16s_pcr3', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_its_pcr1_neat', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_its_pcr2_1_10', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_its_pcr3_fusion', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('brisbane_fluorimetry_16s', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('brisbane_fluorimetry_its', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('brisbane_16s_qpcr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('brisbane_its_qpcr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('brisbane_i6s_pooled', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('brisbane_its_pooled', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('brisbane_16s_reads', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('brisbane_its_reads', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'BASE', ['Sample454'])


    def backwards(self, orm):
        # Deleting model 'SoilTexture'
        db.delete_table(u'BASE_soiltexture')

        # Deleting model 'SoilColour'
        db.delete_table(u'BASE_soilcolour')

        # Deleting model 'PCRPrimer'
        db.delete_table(u'BASE_pcrprimer')

        # Deleting model 'LandUse'
        db.delete_table(u'BASE_landuse')

        # Deleting model 'GeneralEcologicalZone'
        db.delete_table(u'BASE_generalecologicalzone')

        # Deleting model 'BroadVegetationType'
        db.delete_table(u'BASE_broadvegetationtype')

        # Deleting model 'TillageType'
        db.delete_table(u'BASE_tillagetype')

        # Deleting model 'HorizonClassification'
        db.delete_table(u'BASE_horizonclassification')

        # Deleting model 'SoilClassification'
        db.delete_table(u'BASE_soilclassification')

        # Deleting model 'DrainageClassification'
        db.delete_table(u'BASE_drainageclassification')

        # Deleting model 'ProfilePosition'
        db.delete_table(u'BASE_profileposition')

        # Deleting model 'TargetGene'
        db.delete_table(u'BASE_targetgene')

        # Deleting model 'TargetTaxon'
        db.delete_table(u'BASE_targettaxon')

        # Deleting model 'SiteOwner'
        db.delete_table(u'BASE_siteowner')

        # Deleting model 'CollectionSiteHistory'
        db.delete_table(u'BASE_collectionsitehistory')

        # Deleting model 'CollectionSite'
        db.delete_table(u'BASE_collectionsite')

        # Removing M2M table for field positions on 'CollectionSite'
        db.delete_table(db.shorten_name(u'BASE_collectionsite_positions'))

        # Deleting model 'SoilMetagenomicsSample'
        db.delete_table(u'BASE_soilmetagenomicssample')

        # Deleting model 'SequenceConstruct'
        db.delete_table(u'BASE_sequenceconstruct')

        # Deleting model 'ChemicalAnalysis'
        db.delete_table(u'BASE_chemicalanalysis')

        # Deleting model 'SoilSampleDNA'
        db.delete_table(u'BASE_soilsampledna')

        # Deleting model 'Sample454'
        db.delete_table(u'BASE_sample454')


    models = {
        u'BASE.broadvegetationtype': {
            'Meta': {'object_name': 'BroadVegetationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'vegetation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'BASE.chemicalanalysis': {
            'Meta': {'object_name': 'ChemicalAnalysis'},
            'ammonium_nitrogen': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'boron_hot_cacl2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'bpa_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.BPAUniqueID']"}),
            'cacl2_ph': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'clay': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'conductivity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'course_sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'customer': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'dtpa_copper': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dtpa_iron': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dtpa_manganese': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dtpa_zinc': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exc_aluminium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exc_calcium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exc_magnesium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exc_potassium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'exc_sodium': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'fine_sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'gravel': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'h20_ph': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_name_id': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nitrate_nitrogen': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'organic_carbon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'phosphorus_colwell': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'potassium_colwell': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sand': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'silt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sulphur_colwell': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'texture': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'BASE.collectionsite': {
            'Meta': {'object_name': 'CollectionSite'},
            'australian_classification_soil_type': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'collection_depth': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'drainage_classification': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'history': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': u"orm['BASE.CollectionSiteHistory']", 'null': 'True'}),
            'horizon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': (
            'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['BASE.SiteOwner']", 'null': 'True'}),
            'plot_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'positions': ('django.db.models.fields.related.ManyToManyField', [],
                          {'symmetrical': 'False', 'to': u"orm['geo.GPSPosition']", 'null': 'True', 'blank': 'True'}),
            'profile_position': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slope_aspect': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slope_gradient': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'BASE.collectionsitehistory': {
            'Meta': {'object_name': 'CollectionSiteHistory'},
            'crop_rotation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'current_land_use': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'current'", 'to': u"orm['BASE.LandUse']"}),
            'current_vegetation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'environment_event': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'history_report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'previous_land_use': ('django.db.models.fields.related.ForeignKey', [],
                                  {'related_name': "'previous'", 'to': u"orm['BASE.LandUse']"}),
            'tillage': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'BASE.drainageclassification': {
            'Meta': {'object_name': 'DrainageClassification'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'drainage': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'BASE.generalecologicalzone': {
            'Meta': {'object_name': 'GeneralEcologicalZone'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'BASE.horizonclassification': {
            'Meta': {'object_name': 'HorizonClassification'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'horizon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'BASE.landuse': {
            'Meta': {'object_name': 'LandUse'},
            'classification': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'BASE.pcrprimer': {
            'Meta': {'object_name': 'PCRPrimer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'BASE.profileposition': {
            'Meta': {'object_name': 'ProfilePosition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'BASE.sample454': {
            'Meta': {'object_name': 'Sample454'},
            'adelaide_date_shipped_to_agrf_454': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'adelaide_date_shipped_to_agrf_miseq': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'adelaide_date_shipped_to_ramacciotti': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'adelaide_extraction_sample_weight': (
            'django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'adelaide_fluorimetry': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'adelaide_pcr1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'adelaide_pcr2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'adelaide_pcr_inhibition': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'agrf_batch_number': (
            'django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'aurora_purified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [],
                       {'to': u"orm['common.BPAUniqueID']", 'unique': 'True'}),
            'brisbane_16s_mid': (
            'django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'brisbane_16s_pcr1': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_16s_pcr2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_16s_pcr3': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_16s_qpcr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_16s_reads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_fluorimetry_16s': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_fluorimetry_its': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_i6s_pooled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_its_mid': (
            'django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'brisbane_its_pcr1_neat': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_its_pcr2_1_10': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_its_pcr3_fusion': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'brisbane_its_pooled': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_its_qpcr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'brisbane_its_reads': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'date_received': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dna_storage_nunc_plate': ('django.db.models.fields.CharField', [],
                                       {'default': "''", 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'dna_storage_nunc_tube': ('django.db.models.fields.CharField', [],
                                      {'default': "''", 'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'dna_storage_nunc_well_location': (
            'django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sample_id': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [],
                          {'blank': 'True', 'related_name': "'454_submitter'", 'null': 'True',
                           'to': u"orm['bpaauth.BPAUser']"})
        },
        u'BASE.sequenceconstruct': {
            'Meta': {'object_name': 'SequenceConstruct'},
            'adapter_sequence': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'barcode_sequence': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'forward_primer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'primer_sequence': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reverse_primer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'target_region': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'BASE.siteowner': {
            'Meta': {'object_name': 'SiteOwner'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'BASE.soilclassification': {
            'Meta': {'object_name': 'SoilClassification'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'BASE.soilcolour': {
            'Meta': {'object_name': 'SoilColour'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'colour': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'BASE.soilmetagenomicssample': {
            'Meta': {'object_name': 'SoilMetagenomicsSample'},
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [],
                       {'to': u"orm['common.BPAUniqueID']", 'unique': 'True'}),
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collection_site': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['BASE.CollectionSite']"}),
            'contact_scientist': ('django.db.models.fields.related.ForeignKey', [],
                                  {'to': u"orm['bpaauth.BPAUser']", 'null': 'True', 'blank': 'True'}),
            'date_sent_to_sequencing_facility': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dna_extraction_protocol': (
            'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dna_source': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': u"orm['common.DNASource']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'requested_sequence_coverage': (
            'django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'})
        },
        u'BASE.soilsampledna': {
            'Meta': {'object_name': 'SoilSampleDNA'},
            'barcode_label': (
            'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'barcode_sequence': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'dna_conc': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'forward_primer_sequence': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labeled_extract_name': (
            'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'library_layout': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'library_selection': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pcr_primer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['BASE.PCRPrimer']"}),
            'pcr_primer_db_ref': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'pcr_reaction': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'performer': (
            'django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'protocol_ref': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'reverse_primer_sequence': (
            'django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'submitter': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'target_gene': ('django.db.models.fields.related.ForeignKey', [],
                            {'related_name': "'target'", 'to': u"orm['BASE.TargetGene']"}),
            'target_subfragment': ('django.db.models.fields.related.ForeignKey', [],
                                   {'related_name': "'subfragment'", 'to': u"orm['BASE.TargetGene']"}),
            'target_taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['BASE.TargetTaxon']"})
        },
        u'BASE.soiltexture': {
            'Meta': {'object_name': 'SoilTexture'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texture': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'BASE.targetgene': {
            'Meta': {'object_name': 'TargetGene'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'BASE.targettaxon': {
            'Meta': {'object_name': 'TargetTaxon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {})
        },
        u'BASE.tillagetype': {
            'Meta': {'object_name': 'TillageType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tillage': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bpaauth.bpauser': {
            'Meta': {'object_name': 'BPAUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                        'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'project': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True',
                                  'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.bpaproject': {
            'Meta': {'object_name': 'BPAProject'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.bpauniqueid': {
            'Meta': {'object_name': 'BPAUniqueID'},
            'bpa_id': (
            'django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.BPAProject']"})
        },
        u'common.dnasource': {
            'Meta': {'object_name': 'DNASource'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geo.gpsposition': {
            'Meta': {'object_name': 'GPSPosition'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'elevation': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['BASE']