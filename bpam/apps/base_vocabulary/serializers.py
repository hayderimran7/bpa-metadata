from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from .models import *

class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandUse
        fields = ('description', 'note', 'order', 'parent')


class SoilTextureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilTexture
        fields = ('description', 'texture')

class SoilColourSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilColour
        fields = ('colour', 'code')