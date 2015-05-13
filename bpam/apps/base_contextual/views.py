# -*- coding: utf-8 -*-
import djqscsv
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404

from .models import ChemicalAnalysis, CollectionSite, SampleContext


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


class SampleMatrixListView(ListView):
    model = SampleContext
    context_object_name = 'records'
    template_name = 'base_contextual/sample_matrix_list.html'
    queryset = SampleContext.objects.select_related()
    # paginate_by = settings.DEFAULT_PAGINATION


def get_matrix_csv(request):
    qs = SampleContext.objects.values('bpa_id',
                                      'site__location_name',
                                      'analysis__depth',
                                      'analysis__moisture',
                                      'analysis__colour',
                                      'analysis__gravel',
                                      )
    return djqscsv.render_to_csv_response(qs)


class SampleContextListView(ListView):
    model = SampleContext
    context_object_name = 'sample_contexts'
    template_name = 'base_contextual/sample_context_list.html'
    queryset = SampleContext.objects.select_related('bpa_id',
                                                    'horizon_classification1',
                                                    'horizon_classification2',
                                                    'site__current_land_use',
                                                    'site__general_ecological_zone',
                                                    'site__vegetation_type',
                                                    'site__soil_type_australian_classification')
    # paginate_by = settings.DEFAULT_PAGINATION


class SampleContextDetailView(DetailView):
    model = SampleContext
    template_name = 'base_contextual/sample_context_detail.html'

    def get_object(self):
        return get_object_or_404(SampleContext, bpa_id=self.kwargs['bpa_id'])


class ChemicalAnalysisDetailView(DetailView):
    model = ChemicalAnalysis
    context_object_name = 'ca'
    template_name = 'base_contextual/chemicalanalysis_detail.html'

    def get_object(self):
        return get_object_or_404(ChemicalAnalysis, bpa_id=self.kwargs['bpa_id'])
