# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, DetailView

from apps.common.models import BPAMirror
from apps.common.views import DebugOnlyTemplateView
from .models import MMSample
from .models import MetagenomicSequenceFile
from .models import AmpliconSequenceFile
from .models import MMSite


class AmpliconIndexView(TemplateView):
    template_name = 'marine_microbes/amplicon_index.html'


class AmpliconListView(ListView):
    model = AmpliconSequenceFile
    context_object_name = 'amplicon_list'
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


class AmpliconDetailView(DetailView):
    model = AmpliconSequenceFile
    context_object_name = 'metadata'
    template_name = 'base_amplicon/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AmpliconDetailView, self).get_context_data(**kwargs)
        context['mirrors'] = BPAMirror.objects.all()
        context['sequencefiles'] = AmpliconSequenceFile.objects.filter(sample__bpa_id=context['metadata'].bpa_id)
        context['sample'] = context['metadata']  # same name to make common sequence file template work
        return context


class MMView(DebugOnlyTemplateView):
    template_name = 'marine_microbes/index.html'

    def get_context_data(self, **kwargs):
        context = super(MMView, self).get_context_data(**kwargs)
        context['sample_count'] = MMSample.objects.count()
        context['collection_site_count'] = MMSite.objects.count()
        context['metagenomics_file_count'] = MetagenomicSequenceFile.objects.count()
        context['amplicon_count'] = AmpliconSequenceFile.objects.count()
        return context


class SampleListView(ListView):
    model = MMSample
    context_object_name = 'samples'
    template_name = 'marine_microbes/sample_list.html'


class MetagenomicFileListView(ListView):
    model = MetagenomicSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'marine_microbes/metagenomics_file_list.html'


class SampleDetailView(TemplateView):
    template_name = 'marine_microbes/sample_detail.html'


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
