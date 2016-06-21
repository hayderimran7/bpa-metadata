# -*- coding: utf-8 -*-

from itertools import chain
from django.views.generic import TemplateView, ListView, DetailView

from apps.common.models import BPAMirror
from .models import MMSample
from .models import MetagenomicSequenceFile


class MMView(TemplateView):
    template_name = 'marine_microbes/index.html'

    def get_context_data(self, **kwargs):
        context = super(MMView, self).get_context_data(**kwargs)
        context['sample_count'] = MMSample.objects.count()
        context['metagenomics_file_count'] = MetagenomicSequenceFile.objects.count()
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
        context['sequencefiles'] = list(chain(miseqset))
        context['mirrors'] = BPAMirror.objects.all()
        context['disable_run'] = True

        return context


class ContactsView(TemplateView):
    template_name = 'marine_microbes/contacts.html'


class ConsortiumView(TemplateView):
    template_name = 'marine_microbes/consortium.html'
