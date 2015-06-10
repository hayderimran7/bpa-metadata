from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404

from .models import (
    Extraction,
    MetagenomicsSample,
    MetagenomicsSequenceFile,
    MetagenomicsRun)


class IndexView(TemplateView):
    template_name = 'base_metagenomics/index.html'


class FileListView(ListView):
    model = MetagenomicsSequenceFile
    context_object_name = 'files'
    template_name = 'base_metagenomics/file_list.html'


class ExtractionListView(ListView):
    model = Extraction
    context_object_name = 'extractions'

    def get_context_data(self, **kwargs):
        context = super(ExtractionListView, self).get_context_data(**kwargs)
        context['extractions'] = Extraction.objects.all()
        return context


class RunListView(ListView):
    model = MetagenomicsRun
    context_object_name = 'runs'

    def get_context_data(self, **kwargs):
        context = super(RunListView, self).get_context_data(**kwargs)
        context['runs'] = MetagenomicsRun.objects.all()
        return context


class SampleListView(ListView):
    model = MetagenomicsSample
    context_object_name = 'samples'

    def get_context_data(self, **kwargs):
        context = super(SampleListView, self).get_context_data(**kwargs)
        context['samples'] = MetagenomicsSample.objects.all()
        return context


class SampleDetailView(DetailView):
    model = MetagenomicsSample
    context_object_name = 'sample'
    template_name = 'base_metagenomics/metagenomicssample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = MetagenomicsSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        return context

    def get_object(self):
        return get_object_or_404(MetagenomicsSample, bpa_id=self.kwargs['bpa_id'])
