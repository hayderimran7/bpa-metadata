# -*- coding: utf-8 -*-
from django.views.generic import TemplateView, ListView, DetailView

from apps.common.views import DebugOnlyTemplateView
from bpam.views import CKANTemplateView
from .models import MMSample
from .models import MMSite


class AmpliconIndexView(TemplateView):
    template_name = 'marine_microbes/amplicon_index.html'


class AmpliconListView(CKANTemplateView):
    template_name = 'marine_microbes/amplicon_list.html'
    amplicon = 'all'

    def get_context_data(self, **kwargs):
        context = super(AmpliconListView, self).get_context_data(**kwargs)
        context['amplicon'] = self.amplicon
        return context


class Amplicon16SListView(AmpliconListView):
    amplicon = '16s'


class Amplicon18SListView(AmpliconListView):
    amplicon = '18s'


class AmpliconA16SListView(AmpliconListView):
    amplicon = 'a16s'


class MMView(DebugOnlyTemplateView):
    template_name = 'marine_microbes/index.html'


class SampleListView(CKANTemplateView):
    template_name = 'marine_microbes/sample_list.html'


class MetagenomicFileListView(CKANTemplateView):
    template_name = 'marine_microbes/metagenomicsequencefile_list.html'


class CollectionSiteListView(ListView):
    model = MMSite
    template_name = 'marine_microbes/collectionsite_list.html'
    context_object_name = 'sites'


class CollectionSiteDetailView(DetailView):
    model = MMSite
    template_name = 'marine_microbes/collectionsite_detail.html'
    context_object_name = 'collectionsite'

    def get_context_data(self, **kwargs):
        context = super(CollectionSiteDetailView, self).get_context_data(**kwargs)
        context['samples'] = MMSample.objects.filter(site=self.get_object())
        return context
