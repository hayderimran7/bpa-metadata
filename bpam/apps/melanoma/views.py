from django.views.generic import ListView, DetailView
from django.shortcuts import render

from apps.common.models import BPAMirror
from apps.common.views import DebugOnlyTemplateView

from apps.melanoma.models import MelanomaSample, MelanomaSequenceFile, Array


class IndexView(DebugOnlyTemplateView):
    template_name = 'melanoma/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sample_size'] = MelanomaSample.objects.count()
        context['array_size'] = Array.objects.count()
        context['sequence_file_size'] = MelanomaSequenceFile.objects.count()
        return context


class SequenceFileListView(ListView):
    model = MelanomaSequenceFile
    context_object_name = 'sequencefiles'
    queryset = MelanomaSequenceFile.objects.select_related('sample', 'run', 'sample__bpa_id', 'run__sample',
                                                           'url_verification')

    # paginate_by = settings.DEFAULT_PAGINATION

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['mirrors'] = BPAMirror.objects.all()
        return context


class ArrayListView(ListView):
    model = Array
    context_object_name = 'arrays'
    # paginate_by = settings.DEFAULT_PAGINATION


class SampleListView(ListView):
    model = MelanomaSample
    context_object_name = 'samples'
    template_name = 'melanoma/melanoma_sample_list.html'
    queryset = MelanomaSample.objects.select_related('bpa_id', 'contact_scientist', 'tumor_stage', 'dna_source')
    # paginate_by = settings.DEFAULT_PAGINATION


class SampleDetailView(DetailView):
    model = MelanomaSample
    context_object_name = 'sample'
    template_name = 'melanoma/melanoma_sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = MelanomaSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)
        context['mirrors'] = BPAMirror.objects.all()

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
        add_search_results(MelanomaSequenceFile.objects.filter(sample__bpa_id__bpa_id__endswith='/' + term))
        add_search_results(MelanomaSequenceFile.objects.filter(sample__name__icontains=term))

    data['nresults'] += len(data['melanoma_object_list'])
    return render(request, 'melanoma/search_results.html', data)
