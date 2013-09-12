
from django.http import HttpResponse
from django.shortcuts import render
from apps.common.models import BPAUniqueID
from apps.melanoma.models import MelanomaSequenceFile

def search_view(request, term):
    data = {
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
