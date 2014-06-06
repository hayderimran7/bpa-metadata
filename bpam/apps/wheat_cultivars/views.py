from django.views.generic import TemplateView, ListView, DetailView
from django.conf import settings

from .models import *

class CultivarsView(TemplateView):
    template_name = 'wheat_cultivars/index.html'


class SampleListView(ListView):
    model = CultivarSample
    context_object_name = 'samples'
    template_name = 'wheat_cultivars/sample_list.html'
    paginate_by = settings.DEFAULT_PAGINATION


class SampleDetailView(DetailView):
    model = CultivarSample
    context_object_name = 'sample'
    template_name = 'wheat_cultivars/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = CultivarSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)

        return context


class SequenceFileListView(ListView):
    model = CultivarSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'wheat_cultivars/sequencefile_list.html'
    paginate_by = settings.DEFAULT_PAGINATION
