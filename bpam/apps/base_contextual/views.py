from django.views.generic import ListView, DetailView, TemplateView

from .models import ChemicalAnalysis, CollectionSite


class LandingView(TemplateView):
    template_name = 'base_contextual/landing.html'


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
    context_object_name = 'reports'


class CollectionSiteListView(ListView):
    model = CollectionSite
    context_object_name = 'sites'

    def get_context_data(self, **kwargs):
        context = super(CollectionSiteListView, self).get_context_data(**kwargs)
        context['positions'] = CollectionSite.get_json_postitions()
        return context


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    template_name = 'base_contextual/collectionsite_detail.html'
