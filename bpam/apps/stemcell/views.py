# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from bpam.ckan_views import ckan_tracker_refresh
from .models import CKAN_RESOURCE_TYPE_TO_MODEL

from apps.common.views import BaseSampleDetailView, DebugOnlyTemplateView


class StemCellView(DebugOnlyTemplateView):
    template_name = 'stemcell/index.html'


class ProjectOverviewView(TemplateView):
    template_name = 'stemcell/project_overview.html'


class SampleDetailView(BaseSampleDetailView):
    template_name = 'stemcell/sample_detail.html'
    project = 'stemcell'


class CKANRefresh(View):
    def get(self, request):
        ckan_tracker_refresh(CKAN_RESOURCE_TYPE_TO_MODEL)
        return HttpResponse("OK")
