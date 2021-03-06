from rest_framework import serializers

from .models import (LandUse, SoilColour, GeneralEcologicalZone, BroadVegetationType, TillageType,
                     HorizonClassification, AustralianSoilClassification, FAOSoilClassification, DrainageClassification,
                     ProfilePosition)


class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandUse
        fields = ('description', 'note', 'order', 'parent')


class SoilColourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilColour
        fields = ('colour', 'code')


class GeneralEcologicalZoneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GeneralEcologicalZone
        fields = ('description', 'note')


class BroadVegetationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BroadVegetationType
        fields = ('vegetation', 'note')


class TillageTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TillageType
        fields = ('tillage', 'description')


class HorizonClassificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HorizonClassification
        fields = ('horizon', 'description')


class AustralianSoilClassificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AustralianSoilClassification
        fields = ('classification', 'note')


class FAOSoilClassificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FAOSoilClassification
        fields = ('classification', 'note')


class DrainageClassificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DrainageClassification
        fields = ('drainage', 'description')


class ProfilePositionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProfilePosition
        fields = ('position', )
