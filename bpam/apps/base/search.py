from apps.base_contextual.models import CollectionSample
import logging
logger = logging.getLogger("rainbow")


def search_strategy_horizon_desc(searcher):
    for collection_sample in CollectionSample.objects.all():
        if searcher.search_value == collection_sample.get_horizon_description():
            yield collection_sample


class Searcher(object):
    SEARCH_TYPE_RANGE = "RANGE"
    SEARCH_TYPE_FIELD = "FIELD"
    UNSET = "----"
    SEARCH_TABLE = {
        CollectionSample: {"sample_id": "bpa_id__bpa_id",
                           "date_sampled": "site__date_sampled",
                           "lat": "site__lat",
                           "lon": "site__lon",
                           "depth": "depth",
                           "horizon1": "horizon_classification1__horizon",
                           "horizon2": "horizon_classification2__horizon",
                           "description": search_strategy_horizon_desc,
                           "current_land_use": "site__current_land_use__description",
                           "general_ecological_zone": "site__general_ecological_zone__description",
                           "vegetation_type": "site__vegetation_type__vegetation",
                           "vegetation_total_cover": "site__vegetation_total_cover",
                           "vegetation_dominant_trees": "site_vegetation_dominant_trees",
        }
    }

    def _get_matching_samples(self):
        for model_class in Searcher.SEARCH_TABLE:
            if self.search_field in Searcher.SEARCH_TABLE[model_class]:
                search_strategy = Searcher.SEARCH_TABLE[model_class][self.search_field]
                if callable(search_strategy):
                    first_level_results = search_strategy(self)
                else:
                    filter_dict = {search_strategy: self.search_value}
                    first_level_results = model_class.objects.filter(**filter_dict)

                return self._filter_on_taxonomy(first_level_results)

    def _filter_on_taxonomy(self, results):
        return results # TODO filter on taxonommic results





    def __init__(self, parameters):
        logger.debug("searcher search parameters = %s" % parameters)
        self.parameters = parameters
        self.search_field = self.parameters.get("search_field", None)
        self.search_value = self.parameters.get("search_value", None)

        self.search_range = self.parameters.get("search_range", None)
        self.search_range_min = self.parameters.get("search_range_min", None)
        self.search_range_max = self.parameters.get("search_range_max", None)

        self.search_phylum = self.parameters.get("search_phylum", None)
        self.search_class = self.parameters.get("search_class", None)
        self.search_order = self.parameters.get("search_order", None)
        self.search_family = self.parameters.get("search_family", None)
        self.search_genus = self.parameters.get("search_genus", None)

        if self.search_field == Searcher.UNSET:
            self.search_type = Searcher.SEARCH_TYPE_RANGE
            logger.debug("searcher search type = range")
        else:
            self.search_type = Searcher.SEARCH_TYPE_FIELD
            logger.debug("search search type = field")



    def _get_range_search_query(self):

        return []  # todo range search
