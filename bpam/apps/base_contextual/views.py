# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404

from bpam.views import CKANTemplateView
from .models import ChemicalAnalysis, CollectionSite, SampleContext

import sample_context


def get_matrix_csv(request):
    return sample_context.get_matrix_values()


class IndexView(TemplateView):
    template_name = 'base_contextual/index.html'


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
    context_object_name = 'reports'
    queryset = ChemicalAnalysis.objects.select_related('bpa_id', 'colour')  # TODO colour ?
    # paginate_by = settings.DEFAULT_PAGINATION


class CollectionSiteListView(ListView):
    model = CollectionSite
    context_object_name = 'sites'
    queryset = CollectionSite.objects.select_related('current_land_use')


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    template_name = 'base_contextual/collectionsite_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionSiteDetailView, self).get_context_data(**kwargs)
        context['samples'] = SampleContext.objects.filter(site=self.get_object())

        return context


class SampleContextDetailView(DetailView):
    model = SampleContext
    template_name = 'base_contextual/sample_context_detail.html'

    def get_object(self):
        return get_object_or_404(SampleContext, bpa_id=self.kwargs['bpa_id'])

    def get_context_data(self, **kwargs):
        context = super(SampleContextDetailView, self).get_context_data(**kwargs)
        context['ca'] = self.get_object().analysis
        context['collectionsite'] = self.get_object().site

        return context


class SampleMatrixListView(CKANTemplateView):
    template_name = 'base_contextual/sample_matrix_list.html'


class SampleContextListView(ListView):
    model = SampleContext
    context_object_name = 'sample_contexts'
    template_name = 'base_contextual/sample_context_list.html'
    queryset = SampleContext.objects.select_related(
        'bpa_id', 'horizon_classification1', 'horizon_classification2', 'site__current_land_use',
        'site__general_ecological_zone', 'site__vegetation_type', 'site__soil_type_australian_classification')
    # paginate_by = settings.DEFAULT_PAGINATION


class ChemicalAnalysisDetailView(DetailView):
    model = ChemicalAnalysis
    context_object_name = 'ca'
    template_name = 'base_contextual/chemicalanalysis_detail.html'

    def get_object(self):
        return get_object_or_404(ChemicalAnalysis, bpa_id=self.kwargs['bpa_id'])
