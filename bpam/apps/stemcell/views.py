# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from apps.common.views import DebugOnlyTemplateView


class StemCellView(DebugOnlyTemplateView):
    template_name = 'stemcell/index.html'


class ProjectOverviewView(TemplateView):
    template_name = 'stemcell/project_overview.html'


class SampleDetailView(TemplateView):
    template_name = 'stemcell/sample_detail.html'
