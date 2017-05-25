# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from apps.common.models import CKANServer
from collections import OrderedDict

from apps.common.views import DebugOnlyTemplateView
from .models import (GenomicsPacBioTrack,
                     GenomicsMiSeqTrack,
                     TranscriptomicsHiSeqTrack,
                     MetabolomicsLCMSTrack,
                     ProteomicsMS1QuantificationTrack,
                     ProteomicsSwathMSTrack,
                     )
from bpam.ckan_views import ckan_tracker_refresh
from .models import CKAN_RESOURCE_TYPE_TO_MODEL

# a list of sepsis sample track types
tracks = (GenomicsPacBioTrack, GenomicsMiSeqTrack, TranscriptomicsHiSeqTrack, MetabolomicsLCMSTrack, ProteomicsMS1QuantificationTrack, ProteomicsSwathMSTrack)


class SepsisView(DebugOnlyTemplateView):
    template_name = 'sepsis/index.html'


class TrackOverview(TemplateView):
    template_name = 'sepsis/track_overview.html'

    def get_context_data(self, **kwargs):
        context = super(TrackOverview, self).get_context_data(**kwargs)
        return context


class TrackOverviewConstraints(View):
    # query definition is shared with TrackDetails
    constraint_queries = OrderedDict([
        ('Genomics PacBio', lambda: GenomicsPacBioTrack.objects.all()),
        ('Genomics MiSeq', lambda: GenomicsMiSeqTrack.objects.all()),
        ('Transcriptomics HiSeq', lambda: TranscriptomicsHiSeqTrack.objects.all()),
        ('Metabolomics LCMS', lambda: MetabolomicsLCMSTrack.objects.all()),
        ('Proteomics MS1 Quantification', lambda: ProteomicsMS1QuantificationTrack.objects.all()),
        ('Proteomics Swath-MS', lambda: ProteomicsSwathMSTrack.objects.all())
    ])
    state_queries = OrderedDict([
        ('inproc', ('Sample processing', lambda q: q.filter(archive_ingestion_date__isnull=True).filter(data_generated=False))),
        ('bpaarchiveingest', ('BPA Archive Ingest', lambda q: q.filter(archive_ingestion_date__isnull=True).filter(data_generated=True))),
        ('bpaqc', ('BPA QC', None)),
        ('embargoed', ('Embargoed', lambda q: q.filter(contextual_data_submission_date__isnull=False).filter(archive_ingestion_date__isnull=False))),
        ('public', ('Public', None)),
        ('all', (None, lambda q: q.all())),
    ])

    def get(self, request):
        tree = []

        for const, const_query in TrackOverviewConstraints.constraint_queries.items():
            const_result = const_query()
            tree.append({"id": const, "parent": "#", "text": "%s (%d)" % (const, len(const_result))})
            for slug, (status, query) in TrackOverviewConstraints.state_queries.items():
                if status is None:
                    continue
                if query:
                    status_count = len(query(const_result))
                    tree.append({"id": "%s/%s" % (const, slug), "parent": const, "text": "%s (%d)" % (status, status_count)})
                else:
                    tree.append({"id": "%s/%s" % (const, slug), "parent": const, "text": "%s (%d)" % (status, 0)})

        return JsonResponse(tree, safe=False)


class TrackDetails(View):

    def get(self, request, constraint=None, status=None):

        if not constraint and not status:
            raise Http404("No constraint or status provided")

        constraint_q = TrackOverviewConstraints.constraint_queries[constraint]
        _, status_q = TrackOverviewConstraints.state_queries[status]

        result = []
        if status_q:
            result = status_q(constraint_q())

        for r in result:
            r.data_type = r.get_data_type_display()

        json_data = self.to_json(result)

        return JsonResponse(json_data, safe=False)

    def to_json(self, raw_data):
        from django.core import serializers
        json_data = serializers.serialize("json", raw_data)

        return json_data


class CKANTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(CKANTemplateView, self).get_context_data(**kwargs)
        context['ckan_base_url'] = CKANServer.primary().base_url
        return context


class SampleListView(CKANTemplateView):
    template_name = 'sepsis/sample_list.html'


class GenomicsMiseqFileListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(GenomicsMiseqFileListView, self).get_context_data(**kwargs)
        context['description'] = 'Genomics MiSeq'
        context['ckan_data_type'] = 'arp-genomics-miseq'
        return context


class TranscriptomicsHiseqFileListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(TranscriptomicsHiseqFileListView, self).get_context_data(**kwargs)
        context['description'] = 'Transcriptomics HiSeq'
        context['ckan_data_type'] = 'arp-transcriptomics-hiseq'
        return context


class GenomicsPacBioFileListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(GenomicsPacBioFileListView, self).get_context_data(**kwargs)
        context['description'] = 'Genomics PacBio'
        context['ckan_data_type'] = 'arp-genomics-pacbio'
        return context


class MetabolomicsLCMSFileListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(MetabolomicsLCMSFileListView, self).get_context_data(**kwargs)
        context['description'] = 'Metabolomics LCMS Analysis'
        context['ckan_data_type'] = 'arp-metabolomics-lcms'
        return context


class ProteomicsMS1QuantificationFileListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProteomicsMS1QuantificationFileListView, self).get_context_data(**kwargs)
        context['description'] = 'Proteomics MS1 Quantification on DDA Data'
        context['ckan_data_type'] = 'arp-proteomics-ms1quantification'
        return context


class ProteomicsSwathMSListView(CKANTemplateView):
    template_name = 'sepsis/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProteomicsSwathMSListView, self).get_context_data(**kwargs)
        context['description'] = 'Proteomics MS2 Quantification on DIA/Swath Data'
        context['ckan_data_type'] = 'arp-proteomics-swathms'
        return context


class ContactsView(TemplateView):
    template_name = 'sepsis/contacts.html'


class ConsortiumView(TemplateView):
    template_name = 'sepsis/consortium.html'


class CKANRefresh(View):
    def get(self, request):
        ckan_tracker_refresh(CKAN_RESOURCE_TYPE_TO_MODEL)
        return HttpResponse("OK")
