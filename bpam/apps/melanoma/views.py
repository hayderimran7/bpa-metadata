from django.http import HttpResponse
from django.template import RequestContext, loader
from django.views.generic.list import ListView
from django.utils import timezone
from apps.melanoma.models import MelanomaSequenceFile
from django.shortcuts import render
from apps.common.models import BPAUniqueID

class MelanomaSequenceFileListView(ListView):
    model = MelanomaSequenceFile

    def get_queryset(self):
        return MelanomaSequenceFile.objects.select_related('sample', 'run', 'sample__bpa_id', 'run__sample')

    def get_context_data(self, **kwargs):
        context = super(MelanomaSequenceFileListView, self).get_context_data(**kwargs)
        context['catalog'] = 'melanoma'
        return context

def search_view(request, term):
    data = {
        'catalog' : 'melanoma',
        'term' : term,
        'nresults' : 0,
    }
    def add_search_results(k, object_list):
        data[k] = object_list
        data['nresults'] += len(object_list)
    # searches restricted to logged-in users go here
    if request.user.is_authenticated:
        add_search_results(
            'melanoma_object_list',
            MelanomaSequenceFile.objects.filter(sample__bpa_id__bpa_id__endswith='/'+term))
    return render(request, 'common/search_results.html', data)
