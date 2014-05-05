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

