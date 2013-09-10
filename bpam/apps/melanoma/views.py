from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.utils import timezone
from apps.melanoma.models import MelanomaSequenceFile

class MelanomaSequenceFileListView(ListView):
    model = MelanomaSequenceFile

    def get_queryset(self):
        return MelanomaSequenceFile.objects.select_related('sample', 'run', 'sample__bpa_id', 'run__sample')

    def get_context_data(self, **kwargs):
        context = super(MelanomaSequenceFileListView, self).get_context_data(**kwargs)
        return context

