from rest_framework import generics

from .models import *
import serializers


class LandUseReadView(generics.ListAPIView):
    queryset = LandUse.objects.all()
    serializer_class = serializers.LandUseSerializer
    paginate_by = 100


class SoilTextureReadView(generics.ListAPIView):
    queryset = SoilTexture.objects.all()
    serializer_class = serializers.SoilTextureSerializer
    paginate_by = 100


class SoilColourReadView(generics.ListAPIView):
    queryset = SoilColour.objects.all()
    serializer_class = serializers.SoilColourSerializer
    paginate_by = 100


class GeneralEcologicalZoneReadView(generics.ListAPIView):
    queryset = GeneralEcologicalZone.objects.all()
    serializer_class = serializers.GeneralEcologicalZoneSerializer
    paginate_by = 100


class TillageTypeReadView(generics.ListAPIView):
    queryset = TillageType.objects.all()
    serializer_class = serializers.TillageTypeSerializer
    paginate_by = 100


class HorizonClassificationReadView(generics.ListAPIView):
    queryset = HorizonClassification.objects.all()
    serializer_class = serializers.HorizonClassificationSerializer
    paginate_by = 100


class AustralianSoilClassificationReadView(generics.ListAPIView):
    queryset = AustralianSoilClassification.objects.all()
    serializer_class = serializers.AustralianSoilClassificationSerializer
    paginate_by = 100


class FAOSoilClassificationReadView(generics.ListAPIView):
    queryset = FAOSoilClassification.objects.all()
    serializer_class = serializers.FAOSoilClassificationSerializer
    paginate_by = 100


class DrainageClassificationReadView(generics.ListAPIView):
    queryset = DrainageClassification.objects.all()
    serializer_class = serializers.DrainageClassificationSerializer
    paginate_by = 100


class ProfilePositionReadView(generics.ListAPIView):
    queryset = ProfilePosition.objects.all()
    serializer_class = serializers.ProfilePositionSerializer
    paginate_by = 100