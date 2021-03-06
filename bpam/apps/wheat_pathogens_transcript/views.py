from django.views.generic import ListView, DetailView

from apps.common.models import BPAMirror
from apps.common.views import DebugOnlyTemplateView

from .models import (WheatPathogenTranscriptSample, WheatPathogenTranscriptSequenceFile)


class IndexView(DebugOnlyTemplateView):
    template_name = 'wheat_pathogens_transcript/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sample_size'] = WheatPathogenTranscriptSample.objects.count()
        context['sequence_file_size'] = WheatPathogenTranscriptSequenceFile.objects.count()
        return context


class SampleListView(ListView):
    model = WheatPathogenTranscriptSample
    context_object_name = 'samples'
    template_name = 'wheat_pathogens_transcript/sample_list.html'
    # paginate_by = settings.DEFAULT_PAGINATION


class SampleDetailView(DetailView):
    model = WheatPathogenTranscriptSample
    context_object_name = 'sample'
    template_name = 'wheat_pathogens_transcript/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['mirrors'] = BPAMirror.objects.all()
        context['sequencefiles'] = WheatPathogenTranscriptSequenceFile.objects.filter(
            sample__bpa_id=context['sample'].bpa_id)

        return context


class SequenceFileListView(ListView):
    model = WheatPathogenTranscriptSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'wheat_pathogens_transcript/sequencefile_list.html'
    # paginate_by = settings.DEFAULT_PAGINATION
