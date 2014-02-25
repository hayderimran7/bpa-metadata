# -*- coding: utf-8 -*-
from south.v2 import DataMigration

from ..contextual_controlled_vocabularies import load


class Migration(DataMigration):
    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        load(orm)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'base_vocabulary.australiansoilclassification': {
            'Meta': {'object_name': 'AustralianSoilClassification'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base_vocabulary.broadvegetationtype': {
            'Meta': {'object_name': 'BroadVegetationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'vegetation': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'base_vocabulary.drainageclassification': {
            'Meta': {'object_name': 'DrainageClassification'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'drainage': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base_vocabulary.faosoilclassification': {
            'Meta': {'object_name': 'FAOSoilClassification'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base_vocabulary.generalecologicalzone': {
            'Meta': {'object_name': 'GeneralEcologicalZone'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base_vocabulary.horizonclassification': {
            'Meta': {'object_name': 'HorizonClassification'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'horizon': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base_vocabulary.landuse': {
            'Meta': {'object_name': 'LandUse'},
            'classification': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'base_vocabulary.profileposition': {
            'Meta': {'object_name': 'ProfilePosition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'base_vocabulary.soilcolour': {
            'Meta': {'object_name': 'SoilColour'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'colour': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base_vocabulary.soiltexture': {
            'Meta': {'object_name': 'SoilTexture'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texture': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'base_vocabulary.tillagetype': {
            'Meta': {'object_name': 'TillageType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tillage': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['base_vocabulary']
    symmetrical = True
