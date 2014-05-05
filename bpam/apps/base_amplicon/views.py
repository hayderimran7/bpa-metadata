from django.views.generic import ListView, DetailView

from .models import *

class MetadataListView(ListView):
    model = AmpliconSequencingMetadata
    context_object_name = 'metadata_list'
    template_name = 'base_amplicon/metadata_list.html'
    paginate_by = 25


class MetadataView(DetailView):
    model = AmpliconSequencingMetadata
    context_object_name = 'metadata'
    template_name = 'base_amplicon/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MetadataView, self).get_context_data(**kwargs)
        context['sequencefiles'] = AmpliconSequenceFile.objects.filter(sample__bpa_id=context['metadata'].bpa_id)
        context['sample'] = context['metadata']  # same name to make common sequence file template work
        return context