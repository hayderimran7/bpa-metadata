from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import OTUSearchForm

class BaseView(TemplateView):
    template_name = 'base/index.html'


class OTUSearchView(FormView):
    form_class = OTUSearchForm
    template_name = 'base/otu_search.html'
