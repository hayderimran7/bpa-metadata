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

class HostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Host

class BPAProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BPAProject

class BPAUniqueIDSerializer(serializers.ModelSerializer):
    project = BPAProjectSerializer()

    class Meta:
        model = BPAUniqueID
        lookup_field = "bpa_id"

class SepsisSampleSerializer(serializers.HyperlinkedModelSerializer):
    bpa_id = BPAUniqueIDSerializer()
    host = HostSerializer()

    class Meta:
        model = SepsisSample


