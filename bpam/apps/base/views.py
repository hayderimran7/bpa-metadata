from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from .search import Searcher
from .forms import OTUSearchForm
from apps.base_contextual.models import CollectionSample


class BaseView(TemplateView):
    template_name = 'base/index.html'


class AbstractSearchableListView(ListView, FormMixin):
    template_name = 'base/search_results.html'

    def __init__(self, *args, **kwargs):
        super(AbstractSearchableListView, self).__init__(*args, **kwargs)
        self.form_data = {}

    def get(self, request):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        if request.POST:
            self.object_list = self.get_queryset()
        else:
            self.object_list = []
        allow_empty = self.get_allow_empty()
        self.context_object_name = self.get_search_items_name()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, search_form=self.form)

        context["result_type"] = self._get_search_result_type()

        return self.render_to_response(context)

    def _get_search_result_type(self):
        if self.object_list is None:
            return "base_metagenomics"
        else:
            if hasattr(self.object_list, "model"):
                # queryset
                module_name = self.object_list.model.__module__
                if "base_contextual" in module_name:
                    return "base_contextual"
                elif "base_metagenomics" in module_name:
                    return "base_metagenomics"
                else:
                    raise Exception("unknown module: %s" % module_name)

    def get_model(self):
        raise NotImplementedError("get_model subclass responsibility")

    def post(self, request):
        self.form_data = {}
        for key in request.POST:
            self.form_data[key] = request.POST[key]

        return self.get(request)

    def get_form(self, form_class):
        return form_class(data=self.form_data, initial=self.form_data)

    def get_search_items_name(self):
        raise NotImplementedError("get_search_items_name subclass responsibility")

    def _get_filters(self, search_form):
        """
        :param search_form: a django form instance
        :return: a filter dictionary suitable for model.objects.filter(**filters)
        """
        return {}

    def get_queryset(self):
        search_parameters = self.form.data
        if not search_parameters:
            return []
        searcher = Searcher(search_parameters)
        return searcher.get_matching_samples()


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
