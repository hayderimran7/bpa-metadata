from rest_framework import viewsets
from rest_framework import generics

from .models import *
import serializers

class LandUseCreateReadView(generics.ListCreateAPIView):
    queryset = LandUse.objects.all()
    serializer_class = serializers.LandUseSerializer
    paginate_by = 100


class SoilTextureCreateReadView(generics.ListCreateAPIView):
    queryset = SoilTexture.objects.all()
    serializer_class = serializers.SoilTextureSerializer
    paginate_by = 100


class SoilColourCreateReadView(generics.ListCreateAPIView):
    queryset = SoilColour.objects.all()
    serializer_class = serializers.SoilColourSerializer
    paginate_by = 100