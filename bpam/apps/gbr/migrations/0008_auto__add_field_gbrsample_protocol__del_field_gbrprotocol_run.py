# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GBRSample.protocol'
        db.add_column(u'gbr_gbrsample', 'protocol',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gbr.GBRProtocol'], null=True),
                      keep_default=False)

        # Deleting field 'GBRProtocol.run'
        db.delete_column(u'gbr_gbrprotocol', 'run_id')


    def backwards(self, orm):
        # Deleting field 'GBRSample.protocol'
        db.delete_column(u'gbr_gbrsample', 'protocol_id')

        # Adding field 'GBRProtocol.run'
        db.add_column(u'gbr_gbrprotocol', 'run',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gbr.GBRRun'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bpaauth.bpauser': {
            'Meta': {'object_name': 'BPAUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
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
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
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
            'bpa_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'primary_key': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'common.organism': {
            'Meta': {'object_name': 'Organism'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kingdom': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ncbi_classification': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'organism_class': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phylum': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'common.sequencer': {
            'Meta': {'object_name': 'Sequencer'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        u'common.urlverification': {
            'Meta': {'object_name': 'URLVerification'},
            'checked_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'checked_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_note': ('django.db.models.fields.TextField', [], {}),
            'status_ok': ('django.db.models.fields.BooleanField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gbr.collectionevent': {
            'Meta': {'object_name': 'CollectionEvent'},
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collector': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'collector'", 'null': 'True', 'to': u"orm['bpaauth.BPAUser']"}),
            'depth': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.CollectionSite']", 'null': 'True'}),
            'water_ph': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'water_temp': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'gbr.collectionsite': {
            'Meta': {'unique_together': "(('lat', 'lon'),)", 'object_name': 'CollectionSite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'gbr.gbrprotocol': {
            'Meta': {'unique_together': "(('library_type', 'base_pairs', 'library_construction_protocol'),)", 'object_name': 'GBRProtocol'},
            'base_pairs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'library_construction': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'library_construction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'library_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'gbr.gbrrun': {
            'DNA_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'Meta': {'object_name': 'GBRRun'},
            'array_analysis_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'flow_cell_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'passage_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'run_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.GBRSample']"}),
            'sequencer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Sequencer']", 'null': 'True', 'blank': 'True'}),
            'sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"}),
            'whole_genome_sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['common.Facility']"})
        },
        u'gbr.gbrsample': {
            'Meta': {'object_name': 'GBRSample'},
            'bpa_id': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.BPAUniqueID']", 'unique': 'True', 'primary_key': 'True'}),
            'collection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'collection_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.CollectionEvent']", 'null': 'True'}),
            'comments_by_facility': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact_bioinformatician': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bioinformatician'", 'null': 'True', 'to': u"orm['bpaauth.BPAUser']"}),
            'contact_scientist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bpaauth.BPAUser']", 'null': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date_sent_to_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_sequenced': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'debug_note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dna_extraction_protocol': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dna_rna_concentration': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dna_source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.DNASource']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Organism']", 'null': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.GBRProtocol']", 'null': 'True'}),
            'requested_read_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'requested_sequence_coverage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sequencing_data_eta': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sequencing_facility': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.Facility']", 'null': 'True'}),
            'sequencing_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'total_dna_rna_shipped': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'gbr.gbrsequencefile': {
            'Meta': {'object_name': 'GBRSequenceFile'},
            'analysed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'date_received_from_sequencing_facility': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lane_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.GBRRun']"}),
            'sample': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gbr.GBRSample']"}),
            'url_verification': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['common.URLVerification']", 'unique': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['gbr']