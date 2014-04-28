from django.views.generic import TemplateView, ListView, DetailView
from .models import GBRSample

class GBRView(TemplateView):
    template_name = 'gbr/index.html'


class SampleListView(ListView):
    model = GBRSample
    context_object_name = 'samples'
    template_name = 'gbr/gbr_sample_list.html'
    paginate_by = 25


class SampleListDetailView(DetailView):
    model = GBRSample
    context_object_name = 'sample'
    template_name = 'gbr/gbr_sample_detail.html'
