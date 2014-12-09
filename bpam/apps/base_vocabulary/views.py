from rest_framework import viewsets
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