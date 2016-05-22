# -*- coding: utf-8 -*-

from rest_framework import viewsets

from apps.common.admin import BPAUniqueID, BPAProject
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

import serializers

class SepsisSampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sepsis Samples to be viewed or edited.
    """
    queryset = SepsisSample.objects.all()
    serializer_class = serializers.SepsisSampleSerializer

class BPAIDViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BPA ID's to be viewed or edited.
    """
    queryset = BPAUniqueID.objects.all()
    serializer_class = serializers.BPAUniqueIDSerializer

class BPAProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows BPA projects to be viewed or edited.
    """
    queryset = BPAProject.objects.all()
    serializer_class = serializers.BPAProjectSerializer


class HostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Sepsis Hosts to be viewed or edited.
    """
    queryset = Host.objects.all()
    serializer_class = serializers.HostSerializer
