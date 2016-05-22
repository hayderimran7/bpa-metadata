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

class BPAUniqueIDSerializer(serializers.HyperlinkedModelSerializer):
    project = BPAProjectSerializer()

    class Meta:
        model = BPAUniqueID

class SepsisSampleSerializer(serializers.HyperlinkedModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = SepsisSample
        exclude = ("bpa_id", )

