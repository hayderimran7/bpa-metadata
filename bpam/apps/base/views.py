from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .search import Searcher
from .forms import BASESearchForm


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
            if not self.form.is_valid():
                self.object_list = []
            else:
                self.object_list = self.get_queryset()
        else:
            self.object_list = []
        allow_empty = self.get_allow_empty()
        self.context_object_name = self.get_search_items_name()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, search_form=self.form)
        return self.render_to_response(context)

    def get_model(self):
        raise NotImplementedError("get_model subclass responsibility")

    def post(self, request):
        self.form_data = {}
        for key in request.POST:
            self.form_data[key] = request.POST[key]

        return self.get(request)

    def get_form(self, form_class):
        form_instance = form_class(data=self.form_data, initial=self.form_data)
        return self._addcss_attributes(form_instance)

    def _addcss_attributes(self, form):
        """
        bootstrapify
        """
        for field_name in form.fields:
            field_object = form.fields[field_name]
            if hasattr(field_object, "widget"):
                field_object.widget.attrs["class"] = "form-control"
                if field_name in ["search_value"]:
                    field_object.widget.attrs["class"] += " typeahead"
                    field_object.widget.attrs["placeholder"] = "Enter Search Term"
                elif field_name in ["search_field"]:
                    field_object.widget.attrs["class"] += " query-field"

        return form

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


class BASESearchView(AbstractSearchableListView):
    def get_form_class(self):
        return BASESearchForm

    def get_model(self):
        from apps.base.models import BASESample
        return BASESample

    def get_search_items_name(self):
        """
        :return: The name used in the template to refer to the list items
        """
        return "samples"

    def get_allow_empty(self):
        return True

# This view might be better implemented as part of the rest api.
# It just provides data for the bootstrap typeahead widget

from django.http import HttpResponse
from django.views.generic.base import View
import json

from ..base_otu.models import OperationalTaxonomicUnit


class OTUAutoCompleteView(View):
    def get(self, request, thing=None):
        query = request.GET.get("q", None)

        otu_fields = {
            "kingdom": None,
            "phylum": None,
            "class": "otu_class",
            "order": None,
            "family": None,
            "genus": None,
            "species": None,
        }

        response = HttpResponse(content_type="application/json")

        if thing in otu_fields.keys():
            field = otu_fields[thing] or thing
            q = OperationalTaxonomicUnit.objects.filter(**{"%s__icontains" % field: query})
            q = q.order_by(field).distinct(field)
            q = q.values_list("id", field)
            options = [{"id": id, "name": name} for (id, name) in q]
        else:
            response.status_code = 404
            options = []

        json.dump(options, response)
        return response


class AutoCompleteView(View):
    STANDARD_VOCABULARY_TABLE = {
            "agrochemical_additions": None,
            "ammonium_nitrogen": None,
            "australian_soil_classification": "AustralianSoilClassification.classification",
            "boron_hot_cacl2": None,
            "cacl2_ph": None,
            "clay": None,
            "colour": "SoilColour.colour",
            "conductivity": None,
            "course_sand": None,
            "current_land_use": None,
            "date_sampled": None,
            "depth": None,
            "description": None,
            "dtpa_copper": None,
            "dtpa_iron": None,
            "dtpa_manganese": None,
            "dtpa_zinc": None,
            "elevation": None,
            "environment_events": None,
            "exc_aluminium": None,
            "exc_calcium": None,
            "exc_magnesium": None,
            "exc_potassium": None,
            "exc_sodium": None,
            "fao_soil_type": "FAOSoilClassification.classification",
            "fine_sand": None,
            "fire_history": None,
            "fire_intensity": None,
            "general_ecological_zone": None,
            "gravel": None,
            "h20_ph": None,
            "immediate_previous_land_use": None,
            "lat": None,
            "lon": None,
            "moisture": None,
            "nitrate_nitrogen": None,
            "organic_carbon": None,
            "phosphorus_colwell": None,
            "potassium_colwell": None,
            "sample_id": None,
            "sand": None,
            "silt": None,
            "sulphur_colwell": None,
            "texture": "SoilTexture.texture",
            "tillage": "TillageType.tillage",
            "total_carbon": None,
            "total_nitrogen": None,
            "vegetation_dominant_trees": None,
            "vegetation_total_cover": None,
            "vegetation_type": "BroadVegetationType.vegetation",
    }

    def get(self, request, search_field=None):
        response = HttpResponse(content_type="application/json")
        model, field = self._get_standardised_vocab(search_field)

        if model is None:
            #response.status_code = 404
            options = []
        else:
            q = model.objects.all()
            q = q.order_by(field).distinct(field)
            q = q.values_list("id", field)
            options = [{"value": id, "text": name} for (id, name) in q]

        json.dump(options, response)
        return response

    def _get_standardised_vocab(self, search_field):
        vocab = self.STANDARD_VOCABULARY_TABLE.get(search_field, None)
        if vocab is None:
            return None, None
        else:
            model_name, field_name = vocab.split(".")
            from apps.base_vocabulary import models as m
            model = getattr(m, model_name)
            return model, field_name

