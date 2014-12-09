from rest_framework import generics

from .models import *
import serializers

PAGINATE_COUNT = 100


class LandUseReadView(generics.ListAPIView):
    queryset = LandUse.objects.all()
    serializer_class = serializers.LandUseSerializer
    paginate_by = PAGINATE_COUNT


class SoilTextureReadView(generics.ListAPIView):
    queryset = SoilTexture.objects.all()
    serializer_class = serializers.SoilTextureSerializer
    paginate_by = PAGINATE_COUNT


class SoilColourReadView(generics.ListAPIView):
    queryset = SoilColour.objects.all()
    serializer_class = serializers.SoilColourSerializer
    paginate_by = PAGINATE_COUNT


class GeneralEcologicalZoneReadView(generics.ListAPIView):
    queryset = GeneralEcologicalZone.objects.all()
    serializer_class = serializers.GeneralEcologicalZoneSerializer
    paginate_by = PAGINATE_COUNT


class TillageTypeReadView(generics.ListAPIView):
    queryset = TillageType.objects.all()
    serializer_class = serializers.TillageTypeSerializer
    paginate_by = PAGINATE_COUNT


class HorizonClassificationReadView(generics.ListAPIView):
    queryset = HorizonClassification.objects.all()
    serializer_class = serializers.HorizonClassificationSerializer
    paginate_by = PAGINATE_COUNT


class AustralianSoilClassificationReadView(generics.ListAPIView):
    queryset = AustralianSoilClassification.objects.all()
    serializer_class = serializers.AustralianSoilClassificationSerializer
    paginate_by = PAGINATE_COUNT


class FAOSoilClassificationReadView(generics.ListAPIView):
    queryset = FAOSoilClassification.objects.all()
    serializer_class = serializers.FAOSoilClassificationSerializer
    paginate_by = PAGINATE_COUNT


class DrainageClassificationReadView(generics.ListAPIView):
    queryset = DrainageClassification.objects.all()
    serializer_class = serializers.DrainageClassificationSerializer
    paginate_by = PAGINATE_COUNT


class ProfilePositionReadView(generics.ListAPIView):
    queryset = ProfilePosition.objects.all()
    serializer_class = serializers.ProfilePositionSerializer
    paginate_by = PAGINATE_COUNT
