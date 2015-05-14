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
    field_header_map = {
        'site__location_name': 'Collection Site',
        'analysis__depth': 'Horizon',
        'analysis__moisture': 'Moisture',
        'analysis__colour': 'Colour',
        'analysis__gravel': 'Gravel',
        'analysis__texture': 'Texture',
        'analysis__course_sand': 'Course Sand',
        'analysis__fine_sand': 'Fine Sand',
        'analysis__sand': 'Sand',
        'analysis__silt': 'Silt',
        'analysis__clay': 'Clay',
        'analysis__ammonium_nitrogen': 'Ammonium Nitrogen',
        'analysis__nitrate_nitrogen': 'Nitrate Nitrogen',
        'analysis__phosphorus_colwell': 'Phosphoros Colwell',
        'analysis__potassium_colwell': 'Potassium Colwell',
        'analysis__sulphur': 'Sulphur',
        'analysis__organic_carbon': 'Organic Carbon',
        'analysis__conductivity': 'Conductivity',
        'analysis__cacl2_ph': 'CaCl2 pH',
        'analysis__h20_ph': 'H2O pH',
        'analysis__dtpa_copper': 'DTPA Cu',
        'analysis__dtpa_iron': 'DTPA Fe',
        'analysis__dtpa_manganese': 'DTPA Mn',
        'analysis__dtpa_zinc': 'DTPA Zn',
        'analysis__exc_aluminium': 'Exc Al',
        'analysis__exc_calcium': 'Exc Ca',
        'analysis__exc_magnesium': 'Exc Mg',
        'analysis__exc_potassium': 'Exc K',
        'analysis__exc_sodium': 'Exc Na',
        'analysis__boron_hot_cacl2': 'Boron Hot CaCl2',
        'analysis__total_nitrogen': 'Total N',
        'analysis__total_carbon': 'Total C',

    }
    qs = SampleContext.objects.values('bpa_id',
                                      'site__location_name',
                                      'analysis__depth',
                                      'analysis__moisture',
                                      'analysis__colour',
                                      'analysis__gravel',
                                      'analysis__texture',
                                      'analysis__course_sand',
                                      'analysis__fine_sand',
                                      'analysis__sand',
                                      'analysis__silt',
                                      'analysis__clay',
                                      'analysis__ammonium_nitrogen',
                                      'analysis__nitrate_nitrogen',
                                      'analysis__phosphorus_colwell',
                                      'analysis__potassium_colwell',
                                      'analysis__sulphur',
                                      'analysis__organic_carbon',
                                      'analysis__conductivity',
                                      'analysis__cacl2_ph',
                                      'analysis__h20_ph',
                                      'analysis__dtpa_copper',
                                      'analysis__dtpa_iron',
                                      'analysis__dtpa_manganese',
                                      'analysis__dtpa_zinc',
                                      'analysis__exc_aluminium',
                                      'analysis__exc_calcium',
                                      'analysis__exc_magnesium',
                                      'analysis__exc_potassium',
                                      'analysis__exc_sodium',
                                      'analysis__boron_hot_cacl2',
                                      'analysis__total_nitrogen',
                                      'analysis__total_carbon',
                                      )
    return djqscsv.render_to_csv_response(qs, field_header_map=field_header_map)


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
