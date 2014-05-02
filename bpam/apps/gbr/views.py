from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings

from .models import GBRSample, GBRSequenceFile


class GBRView(TemplateView):
    template_name = 'gbr/index.html'


class SampleListView(ListView):
    model = GBRSample
    context_object_name = 'samples'
    template_name = 'gbr/gbr_sample_list.html'
    paginate_by = settings.DEFAULT_PAGINATION


class SampleDetailView(DetailView):
    model = GBRSample
    context_object_name = 'sample'
    template_name = 'gbr/gbr_sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = GBRSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)

        return context


class SequenceFileListView(ListView):
    model = GBRSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'gbr/gbr_sequencefile_list.html'
    paginate_by = settings.DEFAULT_PAGINATION
