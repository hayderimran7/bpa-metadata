# -*- coding: utf-8 -*-

from itertools import chain
from django.views.generic import TemplateView, ListView, DetailView

from apps.common.models import BPAMirror
from .models import MMSample
from .models import MetagenomicSequenceFile
from .models import AmpliconSequenceFile
from .models import MMSite


class AmpliconIndexView(TemplateView):
    template_name = 'marine_microbes/amplicon_index.html'

    def get_context_data(self, **kwargs):
        context = super(AmpliconIndexView, self).get_context_data(**kwargs)
        context['16S_size'] = AmpliconSequenceFile.objects.filter(amplicon='16S').count()
        context['18S_size'] = AmpliconSequenceFile.objects.filter(amplicon='18S').count()
        context['ITS_size'] = AmpliconSequenceFile.objects.filter(amplicon='ITS').count()
        context['A16S_size'] = AmpliconSequenceFile.objects.filter(amplicon='A16S').count()
        context['all_size'] = AmpliconSequenceFile.objects.count()
        context['collection_sites_count'] = MMSite.objects.count()
        return context


class MMSiteListView(ListView):
    model = MMSite
    context_object_name = 'sites'
    template_name = 'marine_microbes/collection_site_list.html'


class AmpliconListView(ListView):
    model = AmpliconSequenceFile
    context_object_name = 'amplicon_list'
    template_name = 'marine_microbes/amplicon_list.html'

    def get_context_data(self, **kwargs):
        context = super(AmpliconListView, self).get_context_data(**kwargs)
        context['amplicon'] = 'all'
        context['amplicon_list'] = AmpliconSequenceFile.objects.select_related("sample")
        return context


class Amplicon16SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(Amplicon16SListView, self).get_context_data(**kwargs)
        context['amplicon'] = '16S'
        context['amplicon_list'] = AmpliconSequenceFile.objects.filter(amplicon='16S')
        return context


class Amplicon18SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(Amplicon18SListView, self).get_context_data(**kwargs)
        context['amplicon'] = '18S'
        context['amplicon_list'] = AmpliconSequenceFile.objects.filter(amplicon='18S')
        return context


class AmpliconITSListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(AmpliconITSListView, self).get_context_data(**kwargs)
        context['amplicon'] = 'ITS'
        context['amplicon_list'] = AmpliconSequenceFile.objects.filter(amplicon='ITS')
        return context


class AmpliconA16SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(AmpliconA16SListView, self).get_context_data(**kwargs)
        context['amplicon'] = 'A16S'
        context['amplicon_list'] = AmpliconSequenceFile.objects.filter(amplicon='A16S')
        return context


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


class MMView(TemplateView):
    template_name = 'marine_microbes/index.html'

    def get_context_data(self, **kwargs):
        context = super(MMView, self).get_context_data(**kwargs)
        context['sample_count'] = MMSample.objects.count()
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


class SampleDetailView(DetailView):
    model = MMSample
    context_object_name = 'sample'
    template_name = 'marine_microbes/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        miseqset = MetagenomicSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        ampliconset = AmpliconSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['sequencefiles'] = list(chain(miseqset, ampliconset))
        context['mirrors'] = BPAMirror.objects.all()
        context['disable_run'] = True

        return context


class ContactsView(TemplateView):
    template_name = 'marine_microbes/contacts.html'


class ConsortiumView(TemplateView):
    template_name = 'marine_microbes/consortium.html'
