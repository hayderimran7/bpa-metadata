from django.views.generic import ListView, DetailView

from .models import MetagenomicsSample, MetagenomicsSequenceFile


class SampleListView(ListView):
    model = MetagenomicsSample
    context_object_name = 'samples'


class SampleDetailView(DetailView):
    model = MetagenomicsSample
    context_object_name = 'sample'
    template_name = 'base_metagenomics/metagenomicssample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = MetagenomicsSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)

        return context
