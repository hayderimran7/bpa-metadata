from django.views.generic import TemplateView


class DebugOnlyTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(DebugOnlyTemplateView, self).get_context_data(**kwargs)
        context['DEBUG_ONLY_VIEW'] = True
        return context
