from django.views.generic import TemplateView


class CultivarsView(TemplateView):
    template_name = 'wheat_cultivars/index.html'

