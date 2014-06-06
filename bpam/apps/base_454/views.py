from django.views.generic import ListView, DetailView

from .models import Sample454


class Sample454ListView(ListView):
    model = Sample454
    context_object_name = 'samples'
    template_name = 'base_454/454_list.html'

class Sample454DetailView(DetailView):
    model = Sample454
    context_object_name = 'sample'
    template_name = 'base_454/454_detail.html'

