from django.views.generic import ListView, DetailView, TemplateView

from .models import ChemicalAnalysis, CollectionSite, CollectionSample


class LandingView(TemplateView):
    template_name = 'base_contextual/index.html'


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
    context_object_name = 'reports'


class CollectionSiteListView(ListView):
    model = CollectionSite
    context_object_name = 'sites'


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    template_name = 'base_contextual/collectionsite_detail.html'


class SampleListView(ListView):
    model = CollectionSample
    context_object_name = 'samples'
    template_name = 'base_contextual/sample_list.html'


class SampleDetailView(DetailView):
    model = CollectionSample
    template_name = 'base_contextual/sample_detail.html'
