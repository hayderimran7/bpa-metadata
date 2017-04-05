import json

from django.views.generic import TemplateView

from apps.common.views import DebugOnlyTemplateView
from bpam import ckan_views, utils


class IndexView(DebugOnlyTemplateView):
    template_name = 'wheat_pathogens/index.html'


class SampleListView(TemplateView):
    template_name = 'wheat_pathogens/sample_list.html'


class SampleDetailView(TemplateView):
    template_name = 'wheat_pathogens/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)

        sample = ckan_views.get_tracker_or_sample(**kwargs)
        context['sample'] = sample
        context['sample_json'] = json.dumps(sample, default=utils.json_encoder)

        return context


class SequenceFileListView(TemplateView):
    template_name = 'wheat_pathogens/sequencefile_list.html'
