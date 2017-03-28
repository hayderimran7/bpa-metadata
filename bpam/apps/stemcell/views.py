# -*- coding: utf-8 -*-

from bpam.ckan_views import ckan_tracker_refresh
from .models import (
    MetabolomicTrack,
    ProteomicTrack,
    SingleCellRNASeqTrack,
    SmallRNATrack,
    TranscriptomeTrack)


from django.http import HttpResponse
from django.views.generic import TemplateView, View

from apps.common.views import DebugOnlyTemplateView


class StemCellView(DebugOnlyTemplateView):
    template_name = 'stemcell/index.html'


class ProjectOverviewView(TemplateView):
    template_name = 'stemcell/project_overview.html'


class SampleDetailView(TemplateView):
    template_name = 'stemcell/sample_detail.html'


class CKANRefresh(View):
    refresh_map = {
        'stemcells-transcriptomics': TranscriptomeTrack,
        'stemcells-smallrna': SmallRNATrack,
        'stemcells-singlecellrnaseq': SingleCellRNASeqTrack,
        'stemcells-metabolomic': MetabolomicTrack,
        'stemcells-transcriptome': TranscriptomeTrack,
        'stemcells-proteomic': ProteomicTrack,
    }

    def get(self, request):
        ckan_tracker_refresh(CKANRefresh.refresh_map)
        return HttpResponse("OK")
