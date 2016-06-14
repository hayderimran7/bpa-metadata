# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.common.models import BPAProject, BPAUniqueID, URLVerification

from .models import (Host,
                     MiseqGenomicsMethod,
                     GenomicsMiseqFile,
                     PacBioGenomicsMethod,
                     GenomicsPacBioFile,
                     ProteomicsMethod,
                     TranscriptomicsMethod,
                     SepsisSample,
                     SampleTrack, )


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


class MiseqGenomicsMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiseqGenomicsMethod


class PacBioGenomicsMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacBioGenomicsMethod


class SepsisSampleSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()
    host = HostSerializer()

    # miseq_files = GenomicsMiseqFileSerializer(source="sepsis_genomicsmiseqfile_files")

    # pacbio_files = GenomicsPacBioFileSerializer(many=True)

    class Meta:
        depth = 1
        model = SepsisSample


class GenomicsMiseqFileSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    method = MiseqGenomicsMethodSerializer()
    url_verification = URLVerificationSerializer()

    class Meta:
        model = GenomicsMiseqFile


class GenomicsPacBioFileSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    method = PacBioGenomicsMethodSerializer()
    url_verification = URLVerificationSerializer()

    class Meta:
        model = GenomicsPacBioFile


class SampleTrackSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()

    class Meta:
        model = SampleTrack