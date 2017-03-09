# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class StemCellView(TemplateView):
    template_name = 'stemcell/index.html'


class ContactsView(TemplateView):
    template_name = 'stemcell/contacts.html'


class ProjectOverviewView(TemplateView):
    template_name = 'stemcell/project_overview.html'


class SampleDetailView(TemplateView):
    template_name = 'stemcell/sample_detail.html'
