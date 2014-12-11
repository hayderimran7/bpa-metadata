from rest_framework import generics

from .models import *
import serializers


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
    serializer_class = serializers.ProfilePositionSerializer
