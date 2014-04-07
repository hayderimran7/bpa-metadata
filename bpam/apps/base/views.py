from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from .forms import OTUSearchForm

class BaseView(TemplateView):
    template_name = 'base/index.html'


class AbstractSearchableListView(ListView, FormMixin):
    def get(self, request, *args, **kwargs):
        form_class  = self.get_form_class()
        self.form = self.get_form(form_class, *args, **kwargs)
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

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_form(self):
        raise NotImplementedError("form class subclass resp")

    def get_search_items_name(self):
        raise NotImplementedError("search_items_name subclass responsibility")


class OTUSearchView(AbstractSearchableListView):
    def get_form_class(self):
        return OTUSearchForm

    def get_model(self):
        from apps.base_metagenomics.models import MetagenomicsSample
        return MetagenomicsSample

    def get_form(self, form_class, *args, **kwargs):
        return form_class()

    def get_search_items_name(self):
        """

        :return: The name used in the template to refer to the list items
        """
        return "samples"

    def get_allow_empty(self):
        return True

    def get_queryset(self):
        # self.form holds search filter
        model = self.get_model()
        return model.objects.all()
