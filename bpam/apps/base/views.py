# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging
import zipfile

from cStringIO import StringIO

from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.views.generic.base import View
from django.shortcuts import render

from django.core.mail import BadHeaderError, send_mail

from apps.common.views import DebugOnlyTemplateView
from apps.base_contextual.models import SampleContext, ChemicalAnalysis, CollectionSite
from apps.base_contextual import sample_context
from apps.base_amplicon.models import AmpliconSequencingMetadata
from apps.base_metagenomics.models import MetagenomicsSample
from apps.base_454.models import Sample454

from search_export import OTUExporter
from ..base_otu.models import OperationalTaxonomicUnit
from .search import Searcher
from .forms import BASESearchForm, RequestAccessForm

logger = logging.getLogger("rainbow")


class InfoView(TemplateView):
    template_name = 'base/info.html'


class BaseView(DebugOnlyTemplateView):
    template_name = 'base/index.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['sample_count'] = SampleContext.objects.count()
        context['site_count'] = CollectionSite.objects.count()
        context['chem_analysis_count'] = ChemicalAnalysis.objects.count()
        context['amplicon_count'] = AmpliconSequencingMetadata.objects.count()
        context['metagenomics_count'] = MetagenomicsSample.objects.count()
        context['454_count'] = Sample454.objects.count()
        return context


class AbstractSearchableListView(ListView, FormMixin):
    template_name = 'base/search_results.html'

    def __init__(self, *args, **kwargs):
        super(AbstractSearchableListView, self).__init__(*args, **kwargs)
        self.form_data = {}

        self.form = None
        self.object_list = None

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
            raise Http404("Empty list and '{class_name}.allow_empty' is False.".format(
                class_name=self.__class__.__name__))

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

    def post(self, request):
        # respond to an ajax call and return a jsonified list of result objects
        response = HttpResponse(content_type="application/json")
        try:
            search_parameters = self._get_search_parameters(request.POST)
            searcher = Searcher(search_parameters)
            results = searcher.complex_search()
        except Exception, ex:
            logger.error("Error occurred during search: request.POST={}".format(request.POST))
            logger.error(ex)
            results = "An error occurred on the server"

        json.dump(results, response)
        return response

    def _get_search_parameters(self, post_data):
        parameters = {}

        parameters["search_all"] = post_data.get("search_all", "")
        parameters["search_operator"] = post_data.get("search_operator", "and")
        parameters["search_kingdom"] = post_data.get("kingdom", None)
        parameters["search_phylum"] = post_data.get("phylum", None)
        parameters["search_class"] = post_data.get("otu_class", None)
        parameters["search_order"] = post_data.get("order", None)
        parameters["search_family"] = post_data.get("family", None)
        parameters["search_genus"] = post_data.get("genus", None)
        parameters["search_species"] = post_data.get("species", None)

        def key_name(prefix, _i):
            return "{}{}".format(prefix, _i)

        i = 0
        finished_collecting = False
        # collect search terms
        search_terms = []
        while not finished_collecting:
            # Every search term must have type field e.g. search_type0 means the search type of the first search term
            # this will be set to "field" or "range"
            # if, say, search_type6 is not in the data, there are only 6 ( 0-5) search terms, so we break out of the loop
            # by setting finished_collecting to True
            search_type_key = key_name("search_type", i)
            if search_type_key in post_data:
                search_type = post_data[search_type_key]
                field = post_data.get(key_name("search_field", i))

                if search_type == "field":
                    # field search ( might be standardised ) - value is a string
                    standardised_value = key_name("search_standardised_value", i)
                    if standardised_value in post_data:
                        value = post_data[standardised_value]
                    else:
                        value = post_data[key_name("search_value", i)]

                elif search_type == "range":
                    # range search - value is a min max pair
                    min_value = post_data[key_name("search_range_min", i)]
                    max_value = post_data[key_name("search_range_max", i)]
                    value = (min_value, max_value)

                else:
                    raise Exception("Unknown search for search term with index {}: {}".format(i, search_type))

                search_terms.append((field, value))
                i += 1

            else:
                finished_collecting = True

        # search terms is a list of (field, value) pairs where value is itself a (min, max) pair
        # for a range search
        parameters["search_terms"] = search_terms
        return parameters


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


class StandardisedVocabularyLookUpView(View):
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
        "current_land_use": "LandUse.description",
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
        "general_ecological_zone": "GeneralEcologicalZone.description",
        "gravel": None,
        "h20_ph": None,
        "immediate_previous_land_use": "LandUse.description",
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
        logger.debug('Get search field from model: {} field: {}'.format(model, field))

        if model is None:
            # response.status_code = 404
            options = []
        else:
            q = model.objects.all()
            q = q.order_by(field).distinct(field)
            code_field = self._get_code_field(model, field)
            q = q.values_list(code_field, field)

            options = [{"value": code, "text": name} for (code, name) in q]

        json.dump(options, response)
        return response

    def _get_code_field(self, model, field):
        exceptions_table = {"SoilColour": "code", }
        return exceptions_table.get(model.__name__, field)

    def _get_standardised_vocab(self, search_field):
        vocab = self.STANDARD_VOCABULARY_TABLE.get(search_field, None)
        if vocab is None:
            return None, None
        else:
            model_name, field_name = vocab.split(".")
            from apps.base_vocabulary import models as m
            model = getattr(m, model_name)
            return model, field_name


class TaxonomyLookUpView(View):
    def get(self, request, level, taxon):
        response = HttpResponse(content_type="application/json")
        if level is None:
            logger.info("taxonomic level is None")
            logger.info("request = {}".forma(request))
            options = []
        else:
            levels = ['kingdom', 'phylum', 'otu_class', 'order', 'family', 'genus', 'species']
            if level not in levels:
                logger.info("Level {level} is not in {levels}".format(level=level, levels=levels))
                logger.info("request = {}".format(request))
                options = []
            else:
                filter_expression = {level: taxon}
                next_lower_level_index = levels.index(level) + 1
                next_lower_level = levels[next_lower_level_index]

                otus = OperationalTaxonomicUnit.objects.filter(**
                                                               filter_expression).order_by(next_lower_level).distinct()
                next_lower_level_values = set([getattr(otu, next_lower_level) for otu in otus])
                options = [{"value": x, "text": x} for x in next_lower_level_values if x != ""]
        json.dump(options, response)
        return response


class RequestAccessView(TemplateView):

    request_template_name = 'base/request_access.html'
    success_template_name = 'base/success.html'
    form_class = RequestAccessForm
    email_template = """\
Name: {}
Affiliation: {}
Email address: {}

Request details:
{}
"""

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.request_template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = self.email_template.format(
                form.cleaned_data['name'],
                form.cleaned_data['affiliation'],
                form.cleaned_data['from_email'],
                form.cleaned_data['message'])
            try:
                send_mail("BASE Access Request", email, settings.DEFAULT_FROM_EMAIL, settings.BASE_REQUEST_LIST)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            return render(request, self.success_template_name, {'form': form})
        else:
            return render(request, self.request_template_name, {'form': form})


class SearchExportView(View):
    def get(self, request):

        ids = request.GET.get("ids", "").split(",")

        kingdom = request.GET.get("kingdom", "")
        phylum = request.GET.get("phylum", "")
        otu_class = request.GET.get("otu_class", "")
        order = request.GET.get("order", "")
        family = request.GET.get("family", "")
        genus = request.GET.get("genus", "")
        species = request.GET.get("species", "")

        zippedfile = StringIO()
        zf = zipfile.ZipFile(zippedfile, mode='w', compression=zipfile.ZIP_DEFLATED)
        zf.writestr('contextual_data.csv', sample_context.get_matrix(ids))

        otu_bacteria_csv = StringIO()
        otu_eukaryotes_csv = StringIO()
        otu_fungi_csv = StringIO()
        otu_archea_csv = StringIO()

        otu_exporter = OTUExporter(kingdom=kingdom,
                                   phylum=phylum,
                                   otu_class=otu_class,
                                   order=order,
                                   family=family,
                                   genus=genus,
                                   species=species)

        otu_bacteria_data, otu_eukaryotes_data, otu_fungi_data, otu_archea_data = otu_exporter.export(
            ids, otu_bacteria_csv, otu_eukaryotes_csv, otu_fungi_csv, otu_archea_csv)

        if otu_bacteria_data:
            zf.writestr('bacteria.csv', otu_bacteria_data.read())

        if otu_eukaryotes_data:
            zf.writestr('eukaryotes.csv', otu_eukaryotes_data.read())

        if otu_fungi_data:
            zf.writestr('fungi.csv', otu_fungi_data.read())

        if otu_archea_data:
            zf.writestr('archea.csv', otu_archea_data.read())

        zf.close()
        zippedfile.flush()
        zippedfile.seek(0)

        response = HttpResponse(zippedfile, content_type='application/zip')
        name = "BPASearchResultsExport.zip"
        response['Content-Disposition'] = 'attachment; filename="%s"' % name
        return response
