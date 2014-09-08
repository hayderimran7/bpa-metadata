from django.views.generic import TemplateView, ListView, DetailView
#from django.conf import settings

from .models import CultivarSample, CultivarSequenceFile


class IndexView(TemplateView):
    template_name = 'wheat_cultivars/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sample_size'] = CultivarSample.objects.count()
        context['sequence_file_size'] = CultivarSequenceFile.objects.count()
        return context


class SampleListView(ListView):
    model = CultivarSample
    context_object_name = 'samples'
    template_name = 'wheat_cultivars/sample_list.html'
    # paginate_by = settings.DEFAULT_PAGINATION


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
    # paginate_by = settings.DEFAULT_PAGINATION


class ContactsView(TemplateView):
    template_name = 'contacts.html'