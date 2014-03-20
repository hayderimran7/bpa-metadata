from django.views.generic.list import ListView
from django.shortcuts import render

from apps.melanoma.models import MelanomaSequenceFile


class MelanomaSequenceFileListView(ListView):
    model = MelanomaSequenceFile

    def get_queryset(self):
        return MelanomaSequenceFile.objects.select_related('sample', 'run', 'sample__bpa_id', 'run__sample',
                                                           'url_verification', 'md5')

    def get_context_data(self, **kwargs):
        context = super(MelanomaSequenceFileListView, self).get_context_data(**kwargs)
        context['catalog'] = 'melanoma'
        return context


def search_view(request, term):
    data = {
        'catalog': 'melanoma',
        'melanoma_object_list': [],
        'term': term,
        'nresults': 0,
    }

    def add_search_results(objects):
        results = data['melanoma_object_list']
        present = set(t.id for t in results)
        for obj in objects:
            if obj.id not in present:
                results.append(obj)

    # searches restricted to logged-in users go here
    if request.user.is_authenticated:
        add_search_results(
            MelanomaSequenceFile.objects.filter(sample__bpa_id__bpa_id__endswith='/' + term))
        add_search_results(
            MelanomaSequenceFile.objects.filter(sample__name__icontains=term)
        )

    data['nresults'] += len(data['melanoma_object_list'])
    return render(request, 'common/search_results.html', data)


def index(request):
    return render(request, 'melanoma/index.html')