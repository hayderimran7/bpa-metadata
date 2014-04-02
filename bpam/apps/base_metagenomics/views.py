from django.views.generic import ListView, DetailView

from .models import MetagenomicsSample


class SampleListView(ListView):
    model = MetagenomicsSample
    context_object_name = 'samples'


class SampleListDetailView(DetailView):
    model = MetagenomicsSample
    template_name = 'base_metagenomics/metagenomicssample_detail.html'
