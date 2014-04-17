from django.views.generic import ListView, DetailView, TemplateView

from .models import ChemicalAnalysis, CollectionSite, SampleContext


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


class SampleContextListView(ListView):
    model = SampleContext
    context_object_name = 'sample_contexts'
    template_name = 'base_contextual/sample_context_list.html'
    paginate_by = 25

class SampleContextDetailView(DetailView):
    model = SampleContext
    template_name = 'base_contextual/sample_context_detail.html'
