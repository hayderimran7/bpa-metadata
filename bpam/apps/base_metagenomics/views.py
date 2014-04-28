from django.views.generic import ListView, DetailView

from .models import MetagenomicsSample


class SampleListView(ListView):
    model = MetagenomicsSample
    context_object_name = 'samples'
    paginate_by = 25

class SampleListDetailView(DetailView):
    model = MetagenomicsSample
    context_object_name = 'sample'
    template_name = 'base_metagenomics/metagenomicssample_detail.html'
