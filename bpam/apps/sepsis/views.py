# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, DetailView
from rest_framework import viewsets

from apps.common.models import BPAMirror
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

class SepsisView(TemplateView):
    template_name = 'sepsis/index.html'

    def get_context_data(self, **kwargs):
        context = super(SepsisView, self).get_context_data(**kwargs)
        context['sample_count'] = SepsisSample.objects.count()
        context['genomics_file_count'] = GenomicsFile.objects.count()
        return context

class SampleListView(ListView):
    model = SepsisSample
    context_object_name = 'samples'
    template_name = 'sepsis/sample_list.html'

class GenomicsFileListView(ListView):
    model = GenomicsFile
    context_object_name = 'sequencefiles'
    template_name = 'sepsis/genomics_file_list.html'

class SampleDetailView(DetailView):
    model = SepsisSample
    context_object_name = 'sample'
    template_name = 'sepsis/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = GenomicsFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['mirrors'] = BPAMirror.objects.all()

        return context


class ContactsView(TemplateView):
    template_name = 'sepsis/contacts.html'

class TranscriptomicsFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sepsis Transcriptomic Sequences
    """
    queryset = TranscriptomicsFile.objects.all()
    serializer_class = serializers.TranscriptomicsFileSerializer

class GenomicsFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sepsis Genomics Sequences
    """
    queryset = GenomicsFile.objects.all()
    serializer_class = serializers.GenomicsFileSerializer

class ProteomicsFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sepsis Proteomics Sequences
    """
    queryset = ProteomicsFile.objects.all()
    serializer_class = serializers.ProteomicsFileSerializer

class SepsisSampleTrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows the tracking of sepsis samples
    """
    queryset = SampleTrack.objects.all()
    serializer_class = serializers.SampleTrackSerializer

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
    lookup_field = "bpa_id"

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
