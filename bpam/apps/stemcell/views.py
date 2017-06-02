# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View

from bpam.ckan_views import ckan_tracker_refresh
from .models import CKAN_RESOURCE_TYPE_TO_MODEL

from apps.common.views import DebugOnlyTemplateView


class StemCellView(DebugOnlyTemplateView):
    template_name = 'stemcell/index.html'


class CKANRefresh(View):
    def get(self, request):
        ckan_tracker_refresh(CKAN_RESOURCE_TYPE_TO_MODEL)
        return HttpResponse("OK")
