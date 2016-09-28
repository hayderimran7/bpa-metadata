# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.common.models import BPAProject, BPAUniqueID, URLVerification

from .models import (Host,
                     MiseqGenomicsMethod,
                     HiseqGenomicsMethod,
                     GenomicsMiseqFile,
                     GenomicsHiseqFile,
                     PacBioGenomicsMethod,
                     GenomicsPacBioFile,
                     SepsisSample,
                     PacBioTrack,
                     MiSeqTrack,
                     RNAHiSeqTrack,
                     MetabolomicsTrack,
                     DeepLCMSTrack,
                     SWATHMSTrack,
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


class MiseqGenomicsMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = MiseqGenomicsMethod


class HiseqGenomicsMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = HiseqGenomicsMethod


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


class GenomicsHiseqFileSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    method = HiseqGenomicsMethodSerializer()
    url_verification = URLVerificationSerializer()

    class Meta:
        model = GenomicsHiseqFile


class GenomicsPacBioFileSerializer(serializers.HyperlinkedModelSerializer):
    sample = SepsisSampleSerializer()
    method = PacBioGenomicsMethodSerializer()
    url_verification = URLVerificationSerializer()

    class Meta:
        model = GenomicsPacBioFile

# Tracking API


class PacBioTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = PacBioTrack


class MiSeqTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = MiSeqTrack


class RNAHiSeqTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = RNAHiSeqTrack


class MetabolomicsTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = MetabolomicsTrack


class DeepLCMSTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = DeepLCMSTrack


class SWATHMSTrackSerializer(serializers.ModelSerializer):
    bpa_id = BPAUniqueIDSerializer()

    class Meta:
        model = SWATHMSTrack
