from django.views.generic import ListView, DetailView

from .models import ChemicalAnalysis, CollectionSite


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
    context_object_name = 'reports'


class CollectionSiteListView(ListView):
    model = CollectionSite
    context_object_name = 'sites'


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    template_name = 'base_contextual/collectionsite_detail.html'
