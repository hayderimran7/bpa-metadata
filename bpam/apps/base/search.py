from apps.base.models import BASESample
from apps.base_contextual.models import SampleContext, ChemicalAnalysis
from apps.base_otu.models import OperationalTaxonomicUnit
from django.db.models import Q
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
    SEARCH_TABLE = {
        SampleContext: {"sample_id": "bpa_id__bpa_id",
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
                        "fao_soil_type": "site__soil_type_fao_classification",
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

    def get_matching_samples(self):
        if self.search_type == Searcher.SEARCH_TYPE_FIELD:
            field = self.search_field
        else:
            field = self.search_range

        for model_class in Searcher.SEARCH_TABLE:
            if field in Searcher.SEARCH_TABLE[model_class]:
                logger.debug("%s in %s" % (field, model_class))
                search_strategy = Searcher.SEARCH_TABLE[model_class][field]
                logger.debug("search strategy = %s" % search_strategy)
                if callable(search_strategy):
                    logger.debug("calling strategy ...")
                    first_level_results = search_strategy(self)
                else:
                    if self.search_type == Searcher.SEARCH_TYPE_FIELD:
                        filter_dict = {search_strategy: self.search_value}
                    elif self.search_type == Searcher.SEARCH_TYPE_RANGE:
                        logger.debug("range search")
                        search_strategy += "__range"
                        filter_dict = {search_strategy: (self.search_range_min, self.search_range_max)}

                    first_level_related_models = model_class.objects.filter(**filter_dict)
                    first_level_results = BASESample.objects.filter(bpa_id__in=[m.bpa_id for m in first_level_related_models])

                logger.debug("filtering on taxonomy if present ..")
                return self._filter_on_taxonomy(first_level_results)

        logger.debug("could not find search field %s in search table" % self.search_field)
        return []

    def _filter_on_taxonomy(self, samples):
        """
        :param results: a query set to filter based on taxonomy
        :return:
        """
        from operator import and_

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

            otus = OperationalTaxonomicUnit.objects.filter(reduce(and_, [Q(tf) for tf in taxonomy_filters]))
            logger.debug("otus matching taxonomic filters = %s" % otus)
            our_ids = [s.bpa_id for s in samples]
            logger.debug("bpa ids of samples from non-taxonommic search = %s" % our_ids)
            from apps.base_otu.models import SampleOTU

            sample_otus = SampleOTU.objects.filter(sample__bpa_id__in=our_ids).filter(otu__in=otus)
            return samples.filter(bpa_id__in=[so.sample.bpa_id for so in sample_otus])
        else:
            return samples

    def __init__(self, parameters):
        logger.debug("searcher search parameters = %s" % parameters)
        self.parameters = parameters
        self.search_field = self.parameters.get("search_field", None)
        self.search_value = self.parameters.get("search_value", None)

        self.search_range = self.parameters.get("search_range", None)
        self.search_range_min = self.parameters.get("search_range_min", None)
        self.search_range_max = self.parameters.get("search_range_max", None)

        self.search_kingdom = self.parameters.get("search_kingdom", None)
        self.search_phylum = self.parameters.get("search_phylum", None)
        self.search_class = self.parameters.get("search_class", None)
        self.search_order = self.parameters.get("search_order", None)
        self.search_family = self.parameters.get("search_family", None)
        self.search_genus = self.parameters.get("search_genus", None)
        self.search_species = self.parameters.get("search_species", None)

        if self.search_field == "":
            self.search_type = Searcher.SEARCH_TYPE_RANGE
            logger.debug("searcher search type = range")
        else:
            self.search_type = Searcher.SEARCH_TYPE_FIELD
            logger.debug("search search type = field")
