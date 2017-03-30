from django.views.generic import TemplateView

from apps.common.views import DebugOnlyTemplateView


class IndexView(DebugOnlyTemplateView):
    template_name = 'wheat_pathogens/index.html'


class SampleListView(TemplateView):
    template_name = 'wheat_pathogens/sample_list.html'


class SampleDetailView(TemplateView):
    template_name = 'wheat_pathogens/sample_detail.html'


class SequenceFileListView(TemplateView):
    template_name = 'wheat_pathogens/sequencefile_list.html'
