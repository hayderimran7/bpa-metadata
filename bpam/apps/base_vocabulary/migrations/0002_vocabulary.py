# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from .. import contextual_controlled_vocabularies as vocab

def load(apps, schema_editor):
    """
    Loads the vocabulary
    """
    BroadVegetationType = apps.get_model("base_vocabulary", "BroadVegetationType")
    for vegetation, note in vocab.BroadVegetationTypeVocabulary:
        t = BroadVegetationType.objects.create()
        t.vegetation = vegetation
        t.note = note
        t.save()

    HorizonClassification = apps.get_model("base_vocabulary", "HorizonClassification")
    for horizon, description in vocab.HorizonClassificationVocabulary:
        t = HorizonClassification.objects.create()
        t.horizon = horizon
        t.description = description
        t.save()

    ProfilePosition = apps.get_model("base_vocabulary", "ProfilePosition")
    for position, _ in vocab.ProfilePositionVocabulary:
        t = ProfilePosition.objects.create(position=position)
        t.save()

    DrainageClassification = apps.get_model("base_vocabulary", "DrainageClassification")
    for drainage, description in vocab.DrainageClassificationVocabulary:
        t = DrainageClassification.objects.create()
        t.drainage = drainage
        t.description = description
        t.save()

    AustralianSoilClassification = apps.get_model("base_vocabulary", "AustralianSoilClassification")
    for classification, note in vocab.AustralianSoilClassificationVocabulary:
        t = AustralianSoilClassification.objects.create()
        t.classification = classification
        t.note = note
        t.save()

    GeneralEcologicalZone = apps.get_model("base_vocabulary", "GeneralEcologicalZone")
    for description, note in vocab.EcologicalZoneVocabulary:
        t = GeneralEcologicalZone.objects.create()
        t.description = description
        t.note = note
        t.save()

    FAOSoilClassification = apps.get_model("base_vocabulary", "FAOSoilClassification")
    for classification, note in vocab.FAOSoilClassificationVocabulary:
        t = FAOSoilClassification.objects.create()
        t.classification = classification
        t.note = note
        t.save()

    SoilColour = apps.get_model("base_vocabulary", "SoilColour")
    for colour, code in vocab.SoilColourVocabulary:
        t = SoilColour.objects.create()
        t.colour = colour
        t.code = code
        t.save()

    SoilTexture = apps.get_model("base_vocabulary", "SoilTexture")
    for texture, description in vocab.SoilTextureVocabulary:
        t = SoilTexture.objects.create()
        t.texture = texture
        t.description = description
        t.save()

    TillageType = apps.get_model("base_vocabulary", "TillageType")
    for tillage, description in vocab.TillageClassificationVocabulary:
        t = TillageType.objects.create()
        t.tillage = tillage
        t.description = description
        t.save()

class Migration(migrations.Migration):

    dependencies = [
        ('base_vocabulary', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load)
    ]
