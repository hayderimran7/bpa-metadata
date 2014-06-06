# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'LandUse'
        db.create_table(u'base_vocabulary_landuse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True,
                                                             to=orm['base_vocabulary.LandUse'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['LandUse'])

        # Adding model 'SoilTexture'
        db.create_table(u'base_vocabulary_soiltexture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('texture', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'base_vocabulary', ['SoilTexture'])

        # Adding model 'SoilColour'
        db.create_table(u'base_vocabulary_soilcolour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('colour', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'base_vocabulary', ['SoilColour'])

        # Adding model 'GeneralEcologicalZone'
        db.create_table(u'base_vocabulary_generalecologicalzone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['GeneralEcologicalZone'])

        # Adding model 'BroadVegetationType'
        db.create_table(u'base_vocabulary_broadvegetationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vegetation', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['BroadVegetationType'])

        # Adding model 'TillageType'
        db.create_table(u'base_vocabulary_tillagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tillage', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'base_vocabulary', ['TillageType'])

        # Adding model 'HorizonClassification'
        db.create_table(u'base_vocabulary_horizonclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('horizon', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'base_vocabulary', ['HorizonClassification'])

        # Adding model 'AustralianSoilClassification'
        db.create_table(u'base_vocabulary_australiansoilclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['AustralianSoilClassification'])

        # Adding model 'FAOSoilClassification'
        db.create_table(u'base_vocabulary_faosoilclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['FAOSoilClassification'])

        # Adding model 'DrainageClassification'
        db.create_table(u'base_vocabulary_drainageclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('drainage', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base_vocabulary', ['DrainageClassification'])

        # Adding model 'ProfilePosition'
        db.create_table(u'base_vocabulary_profileposition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'base_vocabulary', ['ProfilePosition'])


    def backwards(self, orm):
        # Deleting model 'LandUse'
        db.delete_table(u'base_vocabulary_landuse')

        # Deleting model 'SoilTexture'
        db.delete_table(u'base_vocabulary_soiltexture')

        # Deleting model 'SoilColour'
        db.delete_table(u'base_vocabulary_soilcolour')

        # Deleting model 'GeneralEcologicalZone'
        db.delete_table(u'base_vocabulary_generalecologicalzone')

        # Deleting model 'BroadVegetationType'
        db.delete_table(u'base_vocabulary_broadvegetationtype')

        # Deleting model 'TillageType'
        db.delete_table(u'base_vocabulary_tillagetype')

        # Deleting model 'HorizonClassification'
        db.delete_table(u'base_vocabulary_horizonclassification')

        # Deleting model 'AustralianSoilClassification'
        db.delete_table(u'base_vocabulary_australiansoilclassification')

        # Deleting model 'FAOSoilClassification'
        db.delete_table(u'base_vocabulary_faosoilclassification')

        # Deleting model 'DrainageClassification'
        db.delete_table(u'base_vocabulary_drainageclassification')

        # Deleting model 'ProfilePosition'
        db.delete_table(u'base_vocabulary_profileposition')


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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True',
                                                          'to': u"orm['base_vocabulary.LandUse']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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