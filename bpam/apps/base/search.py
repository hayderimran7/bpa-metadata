from apps.base.models import BASESample
from apps.common.models import BPAUniqueID
from apps.base_contextual.models import SampleContext, ChemicalAnalysis
from apps.base_amplicon.models import AmpliconSequencingMetadata
from apps.base_otu.models import OperationalTaxonomicUnit
from apps.base_metagenomics.models import MetagenomicsSample
from django.db.models import Q
from operator import and_, or_
from django.core.urlresolvers import reverse
import re

import logging

logger = logging.getLogger("rainbow")


def search_strategy_horizon_desc(searcher):
    """
    Custom search for horizon desc as this is a method call
    :param searcher: searcher i
    :return: a queryset ( so we chain filters for taxonomy)
    """
    ids = []

    for collection_sample in SampleContext.objects.all():
        if searcher.search_value == collection_sample.get_horizon_description():
            ids.append(collection_sample.bpa_id)

    return SampleContext.objects.filter(bpa_id__in=ids)


class SearchStrategy(object):
    """
    Represents a method of searching for matching samples
    """

    def __init__(self, model, search_path=None, return_model=BASESample):
        self.model = model  # The model class to search over ( e.g. ChemicalAnalysis)
        self.return_model = return_model  # the  related model class ( by BPA ID ) to return
        self.search_path = search_path

    def __call__(self, searcher):
        """
        :param searcher: a Searcher instance ( holds search parameters )
        :return: a queryset of models of type return_model type related via bpa_id
        of those picked out by the search query on the nominated model
        """
        if self.search_path is None:
            search_field = searcher.search_field if searcher.search_type == Searcher.SEARCH_TYPE_FIELD else searcher.search_range
        else:
            search_field = self.search_path  # set when navigating through subobjects of model related via foreign key

        if searcher.search_type == searcher.SEARCH_TYPE_FIELD:
            # field = value
            filter_dict = {search_field: searcher.search_value}
        else:
            # range ( value between max and min )
            filter_dict = {search_field + "__range": (searcher.search_range_min, searcher.search_range_max)}

        logger.debug("SearchStrategy filters = %s" % filter_dict)

        matches = self.model.objects.filter(**filter_dict)
        return self.return_model.objects.filter(bpa_id__in=[match.bpa_id for match in matches])


class Searcher(object):
    SEARCH_TYPE_RANGE = "RANGE"
    SEARCH_TYPE_FIELD = "FIELD"
    UNSET = "----"
    SEARCH_TABLE2 = {

    }
    SEARCH_TABLE = {
        SampleContext: {
                        "date_sampled": "site__date_sampled",
                        "lat": "site__lat",
                        "lon": "site__lon",
                        "depth": "depth",
                        "description": search_strategy_horizon_desc,  # check!
                        "current_land_use": "site__current_land_use__description",
                        "general_ecological_zone": "site__general_ecological_zone__description",
                        "vegetation_type": "site__vegetation_type__vegetation",
                        "vegetation_total_cover": "site__vegetation_total_cover",
                        "vegetation_dominant_trees": "site__vegetation_dominant_trees",
                        "elevation": "site__elevation",
                        "australian_soil_classification": "site__soil_type_australian_classification__classification",
                        "fao_soil_type": "site__soil_type_fao_classification__classification",
                        "immediate_previous_land_use": "site__immediate_previous_land_use",
                        "agrochemical_additions": "site__agrochemical_additions",
                        "tillage": "site__tillage__tillage",
                        "fire_history": "site__fire_history",
                        "fire_intensity": "site__fire_intensity",
                        "environment_events": "site__environment_events",
        },

        ChemicalAnalysis: {
            "moisture": SearchStrategy(ChemicalAnalysis),
            "colour": SearchStrategy(ChemicalAnalysis, search_path="colour__code"),
            "texture": SearchStrategy(ChemicalAnalysis),
            "gravel": SearchStrategy(ChemicalAnalysis),
            "course_sand": SearchStrategy(ChemicalAnalysis),
            "fine_sand": SearchStrategy(ChemicalAnalysis),
            "sand": SearchStrategy(ChemicalAnalysis),
            "silt": SearchStrategy(ChemicalAnalysis),
            "clay": SearchStrategy(ChemicalAnalysis),
            "ammonium_nitrogen": SearchStrategy(ChemicalAnalysis),
            "nitrate_nitrogen": SearchStrategy(ChemicalAnalysis),
            "phosphorus_colwell": SearchStrategy(ChemicalAnalysis),
            "potassium_colwell": SearchStrategy(ChemicalAnalysis),
            "sulphur_colwell": SearchStrategy(ChemicalAnalysis),
            "organic_carbon": SearchStrategy(ChemicalAnalysis),
            "conductivity": SearchStrategy(ChemicalAnalysis),
            "cacl2_ph": SearchStrategy(ChemicalAnalysis),
            "h20_ph": SearchStrategy(ChemicalAnalysis),
            "dtpa_copper": SearchStrategy(ChemicalAnalysis),
            "dtpa_iron": SearchStrategy(ChemicalAnalysis),
            "dtpa_manganese": SearchStrategy(ChemicalAnalysis),
            "dtpa_zinc": SearchStrategy(ChemicalAnalysis),
            "exc_aluminium": SearchStrategy(ChemicalAnalysis),
            "exc_calcium": SearchStrategy(ChemicalAnalysis),
            "exc_magnesium": SearchStrategy(ChemicalAnalysis),
            "exc_potassium": SearchStrategy(ChemicalAnalysis),
            "exc_sodium": SearchStrategy(ChemicalAnalysis),
            "boron_hot_cacl2": SearchStrategy(ChemicalAnalysis),
            "total_nitrogen": SearchStrategy(ChemicalAnalysis),
            "total_carbon": SearchStrategy(ChemicalAnalysis),
        }

    }

    def __init__(self, parameters):
        if parameters["search_all"] == "search_all":
            self.search_all = True
        else:
            self.search_all = False

        self.operator = parameters.get("search_operator", "and")
        self.parameters = parameters
        self.search_terms = self.parameters["search_terms"]

        self.search_kingdom = self.parameters.get("search_kingdom", None)
        self.search_phylum = self.parameters.get("search_phylum", None)
        self.search_class = self.parameters.get("search_class", None)
        self.search_order = self.parameters.get("search_order", None)
        self.search_family = self.parameters.get("search_family", None)
        self.search_genus = self.parameters.get("search_genus", None)
        self.search_species = self.parameters.get("search_species", None)

    def complex_search(self):
        if self.search_all:
            # Immediately return a search filtering on taxonomy only
            return self._get_results(self._filter_on_taxonomy(BASESample.objects.all()))

        # otherwise , filter on the search form's content first

        def get_objects(klass, field_value_pairs):
            filters = []
            for field, value in field_value_pairs:
                if type(value) is type(()):
                    # range filter
                    filter_dict_key = "%s__range" % field
                else:
                    filter_dict_key = field

                filter_dict = {filter_dict_key: value}
                filters.append(filter_dict)

            qterms = [Q(**f) for f in filters]

            if self.operator == "and":
                op = and_
            else:
                op = or_

            return klass.objects.filter(reduce(op, qterms))

        search_model_map = {}  # maps model classes to lists of search paths and values to search for ( single or range)
        bpa_id_sets = []

        for field, value in self.search_terms:
            if field == "sample_id": # special case
                try:
                    bpa_id = BPAUniqueID.objects.get(bpa_id=value)
                    bpa_id_sets.append(set([bpa_id]))
                except BPAUniqueID.DoesNotExist:
                    pass
            else:
                for model_class in self.SEARCH_TABLE:
                    field_map = self.SEARCH_TABLE[model_class]
                    if field in field_map:
                        s = field_map[field]
                        if type(s) is type(""):
                            search_path = s
                        else:
                            if s.search_path:
                                search_path = s.search_path
                            else:
                                search_path = field

                        if not model_class in search_model_map:
                            search_model_map[model_class] = [(search_path, value)]
                        else:
                            search_model_map[model_class].append((search_path, value))



        for model_to_search in search_model_map:
            objects = get_objects(model_to_search, search_model_map[model_to_search])
            bpa_ids = set([obj.bpa_id for obj in objects])
            bpa_id_sets.append(bpa_ids)

        if self.operator == "and":
            bpa_ids = set.intersection(*bpa_id_sets)
        elif self.operator == "or":
            bpa_ids = set.union(*bpa_id_sets)
        else:
            raise Exception("Unknown search operator: %s" % self.operator)

        return self._get_results(self._filter_on_taxonomy(bpa_ids))

    def _get_results(self, bpa_ids):

        # get as much info as we can about these ids ( return list of dictionary with links etc)
        from functools import partial

        detail_view_map = {
            ChemicalAnalysis: 'basecontextual:chemicalanalysisdetail',
            SampleContext: 'basecontextual:sampledetail',
            AmpliconSequencingMetadata: 'base_amplicon:metadata',
            MetagenomicsSample: 'basemetagenomics:sample',
        }

        def get_object_detail_view_link(klass, bpa_id):
            try:
                obj = klass.objects.get(bpa_id=bpa_id)
                return reverse(detail_view_map[klass], args=(obj.pk,))
            except klass.DoesNotExist:
                return ""

        def get_amplicon_links(bpa_id):

            amplicon_type_pattern = re.compile(r"^.*?_\d+?_(.*?)_.*$")
            links = []
            for amplicon in AmpliconSequencingMetadata.objects.filter(bpa_id=bpa_id):
                amplicon_type = amplicon.target
                if not amplicon_type:
                    amplicon_type = "Unknown Target"

                links.append({"amplicon_type": amplicon_type, "amplicon_link": reverse(detail_view_map[AmpliconSequencingMetadata], args=(amplicon.pk,))})

            return links

        ca_link = partial(get_object_detail_view_link, ChemicalAnalysis)
        sc_link = partial(get_object_detail_view_link, SampleContext)
        #am_link = partial(get_object_detail_view_link, AmpliconSequencingMetadata)
        mg_link = partial(get_object_detail_view_link, MetagenomicsSample)


        results = []
        for bpa_id in bpa_ids:
            results.append({"bpa_id": bpa_id.bpa_id,
                            "sc": sc_link(bpa_id),
                            "ca": ca_link(bpa_id),
                            "am": get_amplicon_links(bpa_id),
                            "mg": mg_link(bpa_id)})

        return results

    def _filter_on_taxonomy(self, bpa_ids):
        """
        :param results: a query set to filter based on taxonomy
        :return:
        """
        def query_pair(field, s):
            """
            :param field: E.g family or phylum
            :param s: "rhibo*" or somefullstring  NB. foo*bar or *foobar not supported ( case insensitive search)
            :return: the filtered results
            """
            if s.endswith("*"):
                return field + "__istartswith", s[:-1]
            else:
                return field + "__iexact", s

        taxonomy_filters = []

        if self.search_kingdom:
            taxonomy_filters.append(query_pair("kingdom", self.search_kingdom))
        if self.search_phylum:
            taxonomy_filters.append(query_pair("phylum", self.search_phylum))
        if self.search_class:
            taxonomy_filters.append(query_pair("otu_class", self.search_class))
        if self.search_family:
            taxonomy_filters.append(query_pair("family", self.search_family))
        if self.search_genus:
            taxonomy_filters.append(query_pair("genus", self.search_genus))
        if self.search_order:
            taxonomy_filters.append(query_pair("order", self.search_order))
        if self.search_species:
            taxonomy_filters.append(query_pair("species", self.search_species))

        logger.debug("taxonomic filters = %s" % taxonomy_filters)
        filters = [Q(tf) for tf in taxonomy_filters]
        if filters:
            logger.debug("taxonomy filtering will be performed")
            otus = OperationalTaxonomicUnit.objects.filter(reduce(and_, [Q(tf) for tf in taxonomy_filters]))
            logger.debug("otus matching taxonomic filters = %s" % otus)
            from apps.base_otu.models import SampleOTU
            sample_otus = SampleOTU.objects.filter(sample__bpa_id__in=bpa_ids).filter(otu__in=otus).order_by('sample__bpa_id')
            return set([so.sample.bpa_id for so in sample_otus])
        else:
            logger.debug("no taxonomy filtering will be applied")
            return bpa_ids


