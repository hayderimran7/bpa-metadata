# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.common.models import BPAProject, BPAUniqueID, URLVerification
from apps.common.admin import SequenceFileAdmin

from .models import (
    Host,
    GenomicsMethod,
    GenomicsMiseqFile,
    ProteomicsMethod,
    TranscriptomicsMethod,
    SepsisSample,
    SampleTrack,
)

class URLVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLVerification

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host

class BPAProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPAProject

class BPAUniqueIDSerializer(serializers.ModelSerializer):
    project = BPAProjectSerializer()

    class Meta:
        model = BPAUniqueID
        lookup_field = "bpa_id"

class SepsisSampleSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()
    host = HostSerializer()

    class Meta:
        model = SepsisSample

class GenomicsMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenomicsMethod

class GenomicsMiseqFileSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    method = GenomicsMethodSerializer()
    url_verification = URLVerificationSerializer()

    class Meta:
        model = GenomicsMiseqFile

class SampleTrackSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    class Meta:
        model = SampleTrack
