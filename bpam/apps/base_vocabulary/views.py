from rest_framework import generics
from django.views.generic import TemplateView

from .models import (
    LandUse,
    SoilTexture,
    SoilColour,
    GeneralEcologicalZone,
    BroadVegetationType,
    TillageType,
    HorizonClassification,
    AustralianSoilClassification,
    FAOSoilClassification,
    DrainageClassification,
    ProfilePosition
)

import serializers


class VocabularyView(TemplateView):
    template_name = 'base_vocabulary/vocabulary.html'

    def get_context_data(self, **kwargs):
        context = super(VocabularyView, self).get_context_data(**kwargs)
        context['land_use'] = LandUse.objects.all()
        context['soil_texture'] = SoilTexture.objects.all()
        context['soil_colour'] = SoilColour.objects.all()
        context['ecozone'] = GeneralEcologicalZone.objects.all()
        context['vegetation'] = BroadVegetationType.objects.all()
        context['tillage'] = TillageType.objects.all()
        context['horizon'] = HorizonClassification.objects.all()
        context['aus_soil'] = AustralianSoilClassification.objects.all()
        context['fao_soil'] = FAOSoilClassification.objects.all()
        context['drainage'] = DrainageClassification.objects.all()
        context['profiles'] = ProfilePosition.objects.all()
        return context


class LandUseReadView(generics.ListAPIView):
    queryset = LandUse.objects.all()
    serializer_class = serializers.LandUseSerializer


class SoilTextureReadView(generics.ListAPIView):
    queryset = SoilTexture.objects.all()
    serializer_class = serializers.SoilTextureSerializer


class SoilColourReadView(generics.ListAPIView):
    queryset = SoilColour.objects.all()
    serializer_class = serializers.SoilColourSerializer


class GeneralEcologicalZoneReadView(generics.ListAPIView):
    queryset = GeneralEcologicalZone.objects.all()
    serializer_class = serializers.GeneralEcologicalZoneSerializer


class TillageTypeReadView(generics.ListAPIView):
    queryset = TillageType.objects.all()
    serializer_class = serializers.TillageTypeSerializer


class BroadVegetationTypeView(generics.ListAPIView):
    queryset = BroadVegetationType.objects.all()
    serializer_class = serializers.BroadVegetationTypeSerializer


class HorizonClassificationReadView(generics.ListAPIView):
    queryset = HorizonClassification.objects.all()
    serializer_class = serializers.HorizonClassificationSerializer


class AustralianSoilClassificationReadView(generics.ListAPIView):
    queryset = AustralianSoilClassification.objects.all()
    serializer_class = serializers.AustralianSoilClassificationSerializer


class FAOSoilClassificationReadView(generics.ListAPIView):
    queryset = FAOSoilClassification.objects.all()
    serializer_class = serializers.FAOSoilClassificationSerializer


class DrainageClassificationReadView(generics.ListAPIView):
    queryset = DrainageClassification.objects.all()
    serializer_class = serializers.DrainageClassificationSerializer


class ProfilePositionReadView(generics.ListAPIView):
    queryset = ProfilePosition.objects.all()
    ferializer_class = serializers.ProfilePositionSerializer
