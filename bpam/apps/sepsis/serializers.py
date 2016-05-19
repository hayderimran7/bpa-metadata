# -*- coding: utf-8 -*-

from rest_framework import serializers
from apps.common.admin import SequenceFileAdmin, BPAUniqueID, BPAProject
from .models import (
    Host,
    GenomicsMethod,
    GenomicsFile,
    ProteomicsMethod,
    ProteomicsFile,
    TranscriptomicsMethod,
    TranscriptomicsFile,
    SepsisSample,
    SampleTrack,
)

class BPAProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BPAProject
        extra_kwargs = {
            'url': {'view_name': 'bpaproject-detail',},
        }

class BPAUniqueIDSerializer(serializers.HyperlinkedModelSerializer):
    project = BPAProjectSerializer()

    class Meta:
        model = BPAUniqueID

        extra_kwargs = {
            'url': {'view_name': 'bpauniqueid-detail',},
        }

class SepsisSampleSerializer(serializers.HyperlinkedModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = SepsisSample
        exclude = ("host", )

        extra_kwargs = {
            'url': {'view_name': 'sepsissample-detail', },
        }

