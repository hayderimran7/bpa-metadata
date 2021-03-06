from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from apps.common.models import BPAMirror

from .models import (Extraction, MetagenomicsSample, MetagenomicsSequenceFile, MetagenomicsRun)

import sequence_file_csv_export


def get_file_csv(request):
    return sequence_file_csv_export.get_csv()


class IndexView(TemplateView):
    template_name = 'base_metagenomics/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['extraction_count'] = Extraction.objects.count()
        context['file_count'] = MetagenomicsSequenceFile.objects.count()
        context['sample_count'] = MetagenomicsSample.objects.count()
        return context


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
        context['samples'] = MetagenomicsSample.objects\
            .annotate(metagenomics_file_count=Count('metagenomicssequencefile', distinct=True))\
            .annotate(amplicon_file_count=Count('ampliconsequencefile', distinct=True))
        return context


class SampleDetailView(DetailView):
    model = MetagenomicsSample
    context_object_name = 'sample'
    template_name = 'base_metagenomics/metagenomicssample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = MetagenomicsSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['mirrors'] = BPAMirror.objects.all()
        return context

    def get_object(self):
        return get_object_or_404(MetagenomicsSample, bpa_id=self.kwargs['bpa_id'])
