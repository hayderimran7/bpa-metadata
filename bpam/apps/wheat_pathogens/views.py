from django.views.generic import TemplateView, ListView, DetailView

from apps.common.models import BPAMirror
from .models import PathogenSample, PathogenSequenceFile


class IndexView(TemplateView):
    template_name = 'wheat_pathogens/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sample_size'] = PathogenSample.objects.count()
        context['sequence_file_size'] = PathogenSequenceFile.objects.count()
        return context


class SampleListView(ListView):
    model = PathogenSample
    context_object_name = 'samples'
    template_name = 'wheat_pathogens/sample_list.html'
    # paginate_by = settings.DEFAULT_PAGINATION


class SampleDetailView(DetailView):
    model = PathogenSample
    context_object_name = 'sample'
    template_name = 'wheat_pathogens/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = PathogenSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['mirrors'] = BPAMirror.objects.all()

        return context


class SequenceFileListView(ListView):
    model = PathogenSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'wheat_pathogens/sequencefile_list.html'
    # paginate_by = settings.DEFAULT_PAGINATION


class ContactsView(TemplateView):
    template_name = 'contacts.html'
