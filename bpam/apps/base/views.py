from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from copy import deepcopy

from .forms import OTUSearchForm

class BaseView(TemplateView):
    template_name = 'base/index.html'


class AbstractSearchableListView(ListView, FormMixin):
    def __init__(self, *args, **kwargs):
        super(AbstractSearchableListView, self).__init__(*args, **kwargs)
        self.form_data = {}

    def get(self, request):
        form_class  = self.get_form_class()
        self.form = self.get_form(form_class)
        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        self.context_object_name = self.get_search_items_name()
        if not allow_empty and len(self.object_list) == 0:
             raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, search_form=self.form)

        return self.render_to_response(context)

    def get_model(self):
        raise Exception("Not implemented")

    def post(self, request):
        self.form_data = {}
        for key in request.POST:
            if key != "csrftoken":
                self.form_data[key] = request.POST[key]

        return self.get(request)

    def get_form(self, form_class):
        return form_class(data=self.form_data,initial=self.form_data)

    def get_search_items_name(self):
        raise NotImplementedError("search_items_name subclass responsibility")

    def _get_filters(self, search_form):
        """
        :param search_form: a django form instance
        :return: a filter dictionary suitable for model.objects.filter(**filters)
        """
        return {}



class OTUSearchView(AbstractSearchableListView):
    def get_form_class(self):
        return OTUSearchForm

    def get_model(self):
        from apps.base_metagenomics.models import MetagenomicsSample
        return MetagenomicsSample

    def get_search_items_name(self):
        """
        :return: The name used in the template to refer to the list items
        """
        return "samples"

    def get_allow_empty(self):
        return True

    def _get_filters(self, search_form):

        return {}

    def get_queryset(self):
        # self.form holds search filter
        filters = self._get_filters(self.form)
        model = self.get_model()
        return model.objects.all(**filters)
