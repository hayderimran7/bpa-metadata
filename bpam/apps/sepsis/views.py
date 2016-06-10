# -*- coding: utf-8 -*-

from itertools import chain
from django.views.generic import TemplateView, ListView, DetailView
from rest_framework import viewsets

from apps.common.models import BPAMirror
from apps.common.admin import BPAUniqueID, BPAProject
from .models import (Host,
                     MiseqGenomicsMethod,
                     GenomicsMiseqFile,
                     GenomicsPacBioFile,
                     ProteomicsMethod,
                     ProteomicsFile,
                     TranscriptomicsMethod,
                     TranscriptomicsFile,
                     SepsisSample,
                     SampleTrack, )

import serializers


class SepsisView(TemplateView):
    template_name = 'sepsis/index.html'

    def get_context_data(self, **kwargs):
        context = super(SepsisView, self).get_context_data(**kwargs)
        context['sample_count'] = SepsisSample.objects.count()
        context['genomics_miseq_file_count'] = GenomicsMiseqFile.objects.count(
        )
        context[
            'genomics_pacbio_file_count'] = GenomicsPacBioFile.objects.count()
        return context


class SampleListView(ListView):
    model = SepsisSample
    context_object_name = 'samples'
    template_name = 'sepsis/sample_list.html'


class GenomicsMiseqFileListView(ListView):
    model = GenomicsMiseqFile
    context_object_name = 'sequencefiles'
    template_name = 'sepsis/genomics_file_list.html'


class GenomicsPacBioFileListView(ListView):
    model = GenomicsPacBioFile
    context_object_name = 'sequencefiles'
    template_name = 'sepsis/genomics_pacbio_file_list.html'


class SampleDetailView(DetailView):
    model = SepsisSample
    context_object_name = 'sample'
    template_name = 'sepsis/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        miseqset = GenomicsMiseqFile.objects.filter(
            sample__bpa_id=context['sample'].bpa_id)
        pacbioset = GenomicsPacBioFile.objects.filter(
            sample__bpa_id=context['sample'].bpa_id)
        context['sequencefiles'] = list(chain(miseqset, pacbioset))
        context['mirrors'] = BPAMirror.objects.all()

        return context


class ContactsView(TemplateView):
    template_name = 'sepsis/contacts.html'


class GenomicsMiseqFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sepsis Genomics miseq Sequences
    """
    queryset = GenomicsMiseqFile.objects.all()
    serializer_class = serializers.GenomicsMiseqFileSerializer


class GenomicsPacBioFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Sepsis Genomics pacbio Sequences
    """
    queryset = GenomicsPacBioFile.objects.all()
    serializer_class = serializers.GenomicsPacBioFileSerializer


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
