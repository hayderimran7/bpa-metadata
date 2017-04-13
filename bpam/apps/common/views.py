import json

from django.views.generic import TemplateView

from bpam import ckan_views, utils


class DebugOnlyTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(DebugOnlyTemplateView, self).get_context_data(**kwargs)
        context['DEBUG_ONLY_VIEW'] = True
        return context


class BaseSampleDetailView(TemplateView):
    # To be set in subclasses. Ex.
    # template_name = 'marine_microbes/sample_detail.html'
    # project = 'marine_microbes'
    template_name = None
    project = None

    def get_context_data(self, **kwargs):
        context = super(BaseSampleDetailView, self).get_context_data(**kwargs)

        sample = ckan_views.get_tracker_or_sample(project=self.project, **kwargs)
        context['sample'] = sample
        context['sample_json'] = json.dumps(sample, default=utils.json_encoder)

        return context
