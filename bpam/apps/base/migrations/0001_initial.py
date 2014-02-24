# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'PCRPrimer'
        db.create_table(u'base_pcrprimer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['PCRPrimer'])

        # Adding model 'TargetGene'
        db.create_table(u'base_targetgene', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['TargetGene'])

        # Adding model 'TargetTaxon'
        db.create_table(u'base_targettaxon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['TargetTaxon'])

        # Adding model 'SequenceConstruct'
        db.create_table(u'base_sequenceconstruct', (
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
        db.send_create_signal('base', ['SequenceConstruct'])

        # Adding model 'ChemicalAnalysis'
        db.create_table(u'base_chemicalanalysis', (
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
        db.send_create_signal('base', ['ChemicalAnalysis'])

        # Adding model 'SoilSampleDNA'
        db.create_table(u'base_soilsampledna', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('submitter', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dna_conc', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('protocol_ref', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('library_selection', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('library_layout', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('target_taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.TargetTaxon'])),
            ('target_gene',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='target', to=orm['base.TargetGene'])),
            ('target_subfragment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subfragment',
                                                                                         to=orm['base.TargetGene'])),
            ('pcr_primer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.PCRPrimer'])),
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
        db.send_create_signal('base', ['SoilSampleDNA'])

        # Adding model 'MetagenomicsSample'
        db.create_table(u'base_metagenomicssample', (
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
            ('requested_sequence_coverage', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('collection_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date_sent_to_sequencing_facility', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('debug_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['MetagenomicsSample'])

        # Adding model 'MetagenomicsRun'
        db.create_table(u'base_metagenomicsrun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DNA_extraction_protocol', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('passage_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sequencing_facility',
             self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True,
                                                                   to=orm['common.Facility'])),
            ('whole_genome_sequencing_facility',
             self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True,
                                                                   to=orm['common.Facility'])),
            ('array_analysis_facility',
             self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True,
                                                                   to=orm['common.Facility'])),
            ('sequencer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['common.Sequencer'])),
            ('run_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('flow_cell_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.MetagenomicsSample'])),
        ))
        db.send_create_signal('base', ['MetagenomicsRun'])

        # Adding model 'MetagenomicsSequenceFile'
        db.create_table(u'base_metagenomicssequencefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lane_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_received_from_sequencing_facility',
             self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('analysed', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url_verification',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['common.URLVerification'], unique=True,
                                                                      null=True)),
            ('sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.MetagenomicsSample'])),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.MetagenomicsRun'], null=True)),
        ))
        db.send_create_signal('base', ['MetagenomicsSequenceFile'])

        # Adding model 'Sample454'
        db.create_table(u'base_sample454', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('debug_note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
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
        db.send_create_signal('base', ['Sample454'])

        # Adding model 'LandUse'
        db.create_table(u'base_landuse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classification', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['LandUse'])

        # Adding model 'SiteOwner'
        db.create_table(u'base_siteowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('base', ['SiteOwner'])

        # Adding model 'CollectionSiteHistory'
        db.create_table(u'base_collectionsitehistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_report_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('current_vegetation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('previous_land_use',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='previous', to=orm['base.LandUse'])),
            ('current_land_use',
             self.gf('django.db.models.fields.related.ForeignKey')(related_name='current', to=orm['base.LandUse'])),
            ('crop_rotation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('tillage', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('environment_event', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['CollectionSiteHistory'])

        # Adding model 'CollectionSite'
        db.create_table(u'base_collectionsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('location_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
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
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.CollectionSiteHistory'], null=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.SiteOwner'], null=True)),
            ('note', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('base', ['CollectionSite'])

        # Adding unique constraint on 'CollectionSite', fields ['lat', 'lon']
        db.create_unique(u'base_collectionsite', ['lat', 'lon'])

        # Adding model 'SoilTexture'
        db.create_table(u'base_soiltexture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('texture', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('base', ['SoilTexture'])

        # Adding model 'SoilColour'
        db.create_table(u'base_soilcolour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('colour', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal('base', ['SoilColour'])

        # Adding model 'GeneralEcologicalZone'
        db.create_table(u'base_generalecologicalzone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['GeneralEcologicalZone'])

        # Adding model 'BroadVegetationType'
        db.create_table(u'base_broadvegetationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vegetation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['BroadVegetationType'])

        # Adding model 'TillageType'
        db.create_table(u'base_tillagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tillage', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['TillageType'])

        # Adding model 'HorizonClassification'
        db.create_table(u'base_horizonclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('horizon', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('base', ['HorizonClassification'])

        # Adding model 'SoilClassification'
        db.create_table(u'base_soilclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('authority', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['SoilClassification'])

        # Adding model 'DrainageClassification'
        db.create_table(u'base_drainageclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drainage', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('base', ['DrainageClassification'])

        # Adding model 'ProfilePosition'
        db.create_table(u'base_profileposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('base', ['ProfilePosition'])


    def backwards(self, orm):
        # Removing unique constraint on 'CollectionSite', fields ['lat', 'lon']
        db.delete_unique(u'base_collectionsite', ['lat', 'lon'])

        # Deleting model 'PCRPrimer'
        db.delete_table(u'base_pcrprimer')

        # Deleting model 'TargetGene'
        db.delete_table(u'base_targetgene')

        # Deleting model 'TargetTaxon'
        db.delete_table(u'base_targettaxon')

        # Deleting model 'SequenceConstruct'
        db.delete_table(u'base_sequenceconstruct')

        # Deleting model 'ChemicalAnalysis'
        db.delete_table(u'base_chemicalanalysis')

        # Deleting model 'SoilSampleDNA'
        db.delete_table(u'base_soilsampledna')

        # Deleting model 'MetagenomicsSample'
        db.delete_table(u'base_metagenomicssample')

        # Deleting model 'MetagenomicsRun'
        db.delete_table(u'base_metagenomicsrun')

        # Deleting model 'MetagenomicsSequenceFile'
        db.delete_table(u'base_metagenomicssequencefile')

        # Deleting model 'Sample454'
        db.delete_table(u'base_sample454')

        # Deleting model 'LandUse'
        db.delete_table(u'base_landuse')

        # Deleting model 'SiteOwner'
        db.delete_table(u'base_siteowner')

        # Deleting model 'CollectionSiteHistory'
        db.delete_table(u'base_collectionsitehistory')

        # Deleting model 'CollectionSite'
        db.delete_table(u'base_collectionsite')

        # Deleting model 'SoilTexture'
        db.delete_table(u'base_soiltexture')

        # Deleting model 'SoilColour'
        db.delete_table(u'base_soilcolour')

        # Deleting model 'GeneralEcologicalZone'
        db.delete_table(u'base_generalecologicalzone')

        # Deleting model 'BroadVegetationType'
        db.delete_table(u'base_broadvegetationtype')

        # Deleting model 'TillageType'
        db.delete_table(u'base_tillagetype')

        # Deleting model 'HorizonClassification'
        db.delete_table(u'base_horizonclassification')

        # Deleting model 'SoilClassification'
        db.delete_table(u'base_soilclassification')

        # Deleting model 'DrainageClassification'
        db.delete_table(u'base_drainageclassification')

        # Deleting model 'ProfilePosition'
        db.delete_table(u'base_profileposition')


    models = {
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
        'base.broadvegetationtype': {
            'Meta': {'object_name': 'BroadVegetationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'vegetation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'base.chemicalanalysis': {
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
        'base.collectionsite': {
            'Meta': {'unique_together': "(('lat', 'lon'),)", 'object_name': 'CollectionSite'},
            'australian_classification_soil_type': (
            'django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'collection_depth': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'drainage_classification': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'history': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['base.CollectionSiteHistory']", 'null': 'True'}),
            'horizon': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': (
            'django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.SiteOwner']", 'null': 'True'}),
            'plot_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'profile_position': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slope_aspect': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slope_gradient': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'base.collectionsitehistory': {
            'Meta': {'object_name': 'CollectionSiteHistory'},
            'crop_rotation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'current_land_use': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'current'", 'to': "orm['base.LandUse']"}),
            'current_vegetation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'environment_event': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'history_report_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'previous_land_use': ('django.db.models.fields.related.ForeignKey', [],
                                  {'related_name': "'previous'", 'to': "orm['base.LandUse']"}),
            'tillage': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'base.drainageclassification': {
            'Meta': {'object_name': 'DrainageClassification'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'drainage': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.generalecologicalzone': {
            'Meta': {'object_name': 'GeneralEcologicalZone'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.horizonclassification': {
            'Meta': {'object_name': 'HorizonClassification'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'horizon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.landuse': {
            'Meta': {'object_name': 'LandUse'},
            'classification': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.metagenomicsrun': {
            'DNA_extraction_protocol': (
            'django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'MetagenomicsRun'},
            'array_analysis_facility': ('django.db.models.fields.related.ForeignKey', [],
                                        {'blank': 'True', 'related_name': "'+'", 'null': 'True',
                                         'to': u"orm['common.Facility']"}),
            'flow_cell_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passage_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.MetagenomicsSample']"}),
            'sequencer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Sequencer']"}),
            'sequencing_facility': ('django.db.models.fields.related.ForeignKey', [],
                                    {'blank': 'True', 'related_name': "'+'", 'null': 'True',
                                     'to': u"orm['common.Facility']"}),
            'whole_genome_sequencing_facility': ('django.db.models.fields.related.ForeignKey', [],
                                                 {'blank': 'True', 'related_name': "'+'", 'null': 'True',
                                                  'to': u"orm['common.Facility']"})
        },
        'base.metagenomicssample': {
            'Meta': {'object_name': 'MetagenomicsSample'},
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [],
                       {'to': u"orm['common.BPAUniqueID']", 'unique': 'True'}),
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'contact_scientist': ('django.db.models.fields.related.ForeignKey', [],
                                  {'to': u"orm['bpaauth.BPAUser']", 'null': 'True', 'blank': 'True'}),
            'date_sent_to_sequencing_facility': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debug_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dna_extraction_protocol': (
            'django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dna_source': ('django.db.models.fields.related.ForeignKey', [],
                           {'to': u"orm['common.DNASource']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'requested_sequence_coverage': (
            'django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        'base.metagenomicssequencefile': {
            'Meta': {'object_name': 'MetagenomicsSequenceFile'},
            'analysed': (
            'django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'date_received_from_sequencing_facility': (
            'django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filename': (
            'django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lane_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.MetagenomicsRun']", 'null': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.MetagenomicsSample']"}),
            'url_verification': ('django.db.models.fields.related.OneToOneField', [],
                                 {'to': u"orm['common.URLVerification']", 'unique': 'True', 'null': 'True'})
        },
        'base.pcrprimer': {
            'Meta': {'object_name': 'PCRPrimer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.profileposition': {
            'Meta': {'object_name': 'ProfilePosition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'base.sample454': {
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
            'debug_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
        'base.sequenceconstruct': {
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
        'base.siteowner': {
            'Meta': {'object_name': 'SiteOwner'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'base.soilclassification': {
            'Meta': {'object_name': 'SoilClassification'},
            'authority': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.soilcolour': {
            'Meta': {'object_name': 'SoilColour'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'colour': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'base.soilsampledna': {
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
            'pcr_primer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.PCRPrimer']"}),
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
                            {'related_name': "'target'", 'to': "orm['base.TargetGene']"}),
            'target_subfragment': ('django.db.models.fields.related.ForeignKey', [],
                                   {'related_name': "'subfragment'", 'to': "orm['base.TargetGene']"}),
            'target_taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.TargetTaxon']"})
        },
        'base.soiltexture': {
            'Meta': {'object_name': 'SoilTexture'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texture': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'base.targetgene': {
            'Meta': {'object_name': 'TargetGene'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'base.targettaxon': {
            'Meta': {'object_name': 'TargetTaxon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {})
        },
        'base.tillagetype': {
            'Meta': {'object_name': 'TillageType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tillage': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
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
        u'common.facility': {
            'Meta': {'object_name': 'Facility'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.sequencer': {
            'Meta': {'object_name': 'Sequencer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        u'common.urlverification': {
            'Meta': {'object_name': 'URLVerification'},
            'checked_at': (
            'django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'checked_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_note': ('django.db.models.fields.TextField', [], {}),
            'status_ok': ('django.db.models.fields.BooleanField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['base']