# -*- coding: utf-8 -*-

from django.http import Http404
from itertools import chain
from django.views.generic import TemplateView, ListView, DetailView, View
from rest_framework import viewsets
from django.http import JsonResponse

from apps.common.models import BPAMirror
from apps.common.admin import BPAUniqueID, BPAProject
from .models import (Host,
                     GenomicsMiseqFile,
                     TranscriptomicsHiseqFile,
                     GenomicsPacBioFile,
                     SepsisSample,
                     PacBioTrack,
                     MiSeqTrack,
                     RNAHiSeqTrack,
                     MetabolomicsTrack,
                     DeepLCMSTrack,
                     SWATHMSTrack,
                     )

import serializers

# a list of sepsis sample track types
tracks = (PacBioTrack, MiSeqTrack, RNAHiSeqTrack, MetabolomicsTrack, DeepLCMSTrack, SWATHMSTrack)


class SepsisView(TemplateView):
    template_name = 'sepsis/index.html'

    def get_context_data(self, **kwargs):
        context = super(SepsisView, self).get_context_data(**kwargs)
        context['sample_count'] = SepsisSample.objects.count()
        context['genomics_miseq_file_count'] = GenomicsMiseqFile.objects.count()
        context['transcriptomics_hiseq_file_count'] = TranscriptomicsHiseqFile.objects.count()
        context['genomics_pacbio_file_count'] = GenomicsPacBioFile.objects.count()
        context['track_count'] = sum(t.objects.count() for t in tracks)
        return context


class SampleListView(ListView):
    model = SepsisSample
    context_object_name = 'samples'
    template_name = 'sepsis/sample_list.html'

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        context['samples'] = SepsisSample.objects.exclude(strain_or_isolate__isnull=True).exclude(
            strain_or_isolate__exact='')
        return context


class TrackListView(ListView):
    template_name = 'sepsis/track_list.html'

    def get_queryset(self):
        return chain(*(t.objects.all() for t in tracks))

    def get_context_data(self, **kwargs):
        context = super(TrackListView, self).get_context_data(**kwargs)
        context['sampletracks'] = self.get_queryset()
        return context


class TrackOverview(TemplateView):
    template_name = 'sepsis/track_overview.html'

    def get_context_data(self, **kwargs):
        context = super(TrackOverview, self).get_context_data(**kwargs)
        return context


class TrackOverviewConstraints(View):

    def get(self, request):

        constraint_queries = [
            ( 'PacBio', lambda: PacBioTrack.objects.all() ),
            ( 'MiSeq', lambda: MiSeqTrack.objects.all() ),
            ( 'HiSeq', lambda: RNAHiSeqTrack.objects.all() ),
            ( 'Metabolomics', lambda: MetabolomicsTrack.objects.all() ),
            ( 'DeepLCMS', lambda: DeepLCMSTrack.objects.all() ),
            ( 'SWATHMS', lambda: SWATHMSTrack.objects.all() )
        ]
        
        state_queries = [
            ( 'Complete', 'complete', lambda q: q.filter(contextual_data_submission_date__isnull=False).filter(archive_ingestion_date__isnull=False) ),
            ( 'Contextual Data Needed', 'ctdata', lambda q: q.filter(contextual_data_submission_date__isnull=True) ),
            ( 'In processing', 'inproc', lambda q: q.filter(sample_submission_date__isnull=False).filter(archive_ingestion_date__isnull=True) ),
            ( 'Not submitted', 'unsub', lambda q: q.filter(sample_submission_date__isnull=True) ),
        ]

        tree = []
        
        for const, const_query in constraint_queries:
            const_result = const_query()
            tree.append({ "id" : const, "parent" : "#", "text" : "%s (%d)" % (const, len(const_result)) })
            for status, slug, query in state_queries:
                status_count = len(query(const_result))
                tree.append({ "id": "%s/%s" % (const, slug), "parent" : const, "text" : "%s (%d)" % (status, status_count) })
        
        return JsonResponse(tree, safe=False)


class TrackDetails(View):

    def get(self, request, constraint=None, status=None):

        if not constraint and not status:
            raise Http404("No constraint or status provided")

        constraint_queries = {
            'PacBio': lambda: PacBioTrack.objects.all(),
            'MiSeq': lambda: MiSeqTrack.objects.all(),
            'HiSeq': lambda: RNAHiSeqTrack.objects.all(),
            'Metabolomics': lambda: MetabolomicsTrack.objects.all(),
            'DeepLCMS': lambda: DeepLCMSTrack.objects.all(),
            'SWATHMS': lambda: SWATHMSTrack.objects.all(),
        }

        state_queries = {
            'complete': lambda q: q.filter(contextual_data_submission_date__isnull=False).filter(archive_ingestion_date__isnull=False),
            'ctdata': lambda q: q.filter(contextual_data_submission_date__isnull=True),
            'inproc': lambda q: q.filter(sample_submission_date__isnull=False).filter(archive_ingestion_date__isnull=True),
            'unsub': lambda q: q.filter(sample_submission_date__isnull=True),
        }
        
        if constraint == "All":
            assert False
        
        constraint_q = constraint_queries[constraint]
        status_q = state_queries[status]
        
        result = status_q(constraint_q())
        
        for r in result:
            r.data_type = r.get_data_type_display()
        
        json_data = self.to_json(result)
        
        return JsonResponse(json_data, safe=False)

    def to_json(self, raw_data):
        from django.core import serializers
        json_data = serializers.serialize("json", raw_data)
        
        return json_data


class GenomicsMiseqFileListView(ListView):
    model = GenomicsMiseqFile
    context_object_name = 'sequencefiles'
    template_name = 'sepsis/genomics_file_list.html'


class TranscriptomicsHiseqFileListView(ListView):
    model = TranscriptomicsHiseqFile
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
        miseqset = GenomicsMiseqFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        hiseqset = TranscriptomicsHiseqFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        pacbioset = GenomicsPacBioFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['sequencefiles'] = list(chain(miseqset, hiseqset, pacbioset))
        context['mirrors'] = BPAMirror.objects.all()
        context['disable_run'] = True

        return context


class ContactsView(TemplateView):
    template_name = 'sepsis/contacts.html'


class ConsortiumView(TemplateView):
    template_name = 'sepsis/consortium.html'


class GenomicsMiseqFileViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for Sepsis Genomics miseq Sequences
    '''
    queryset = GenomicsMiseqFile.objects.all()
    serializer_class = serializers.GenomicsMiseqFileSerializer


class TranscriptomicsHiseqFileViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for Sepsis Genomics miseq Sequences
    '''
    queryset = TranscriptomicsHiseqFile.objects.all()
    serializer_class = serializers.TranscriptomicsHiseqFileSerializer


class GenomicsPacBioFileViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint for Sepsis Genomics pacbio Sequences
    '''
    queryset = GenomicsPacBioFile.objects.all()
    serializer_class = serializers.GenomicsPacBioFileSerializer


class PacBioTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of PacBio
    '''
    queryset = PacBioTrack.objects.all()
    serializer_class = serializers.PacBioTrackSerializer


class MiSeqTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of MiSeq
    '''
    queryset = MiSeqTrack.objects.all()
    serializer_class = serializers.MiSeqTrackSerializer


class RNAHiSeqTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of RNAHiSeq
    '''
    queryset = RNAHiSeqTrack.objects.all()
    serializer_class = serializers.RNAHiSeqTrackSerializer


class MetabolomicsTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of Metabolomics
    '''
    queryset = MetabolomicsTrack.objects.all()
    serializer_class = serializers.MetabolomicsTrackSerializer


class DeepLCMSTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of Deep LC-MS
    '''
    queryset = DeepLCMSTrack.objects.all()
    serializer_class = serializers.DeepLCMSTrackSerializer


class SWATHMSTrackViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows the tracking of SWAT HMST
    '''
    queryset = SWATHMSTrack.objects.all()
    serializer_class = serializers.SWATHMSTrackSerializer


class SepsisSampleViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows Sepsis Samples to be viewed or edited.
    '''
    queryset = SepsisSample.objects.all()
    serializer_class = serializers.SepsisSampleSerializer


class BPAIDViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows BPA ID's to be viewed or edited.
    '''
    queryset = BPAUniqueID.objects.all()
    serializer_class = serializers.BPAUniqueIDSerializer
    lookup_field = 'bpa_id'


class BPAProjectViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows BPA projects to be viewed or edited.
    '''
    queryset = BPAProject.objects.all()
    serializer_class = serializers.BPAProjectSerializer


class HostViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    API endpoint that allows Sepsis Hosts to be viewed or edited.
    '''
    queryset = Host.objects.all()
    serializer_class = serializers.HostSerializer
