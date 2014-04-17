from django.test import TestCase
from model_mommy import mommy

from apps.base.search import Searcher
from apps.common.models import *
from apps.base.models import *
from apps.base_otu.models import *
from apps.base_contextual.models import *


class SearchTestCase(TestCase):
    def setUp(self):
        super(SearchTestCase, self).setUp()
        self.BASE_sample = mommy.make(BASESample)
        self.bpa_id = self.BASE_sample.bpa_id
        self.collection_site = mommy.make(CollectionSite)

        self.collection_sample = mommy.make(SampleContext, bpa_id=self.bpa_id, site=self.collection_site)
        self.chemical_analysis = mommy.make(ChemicalAnalysis, bpa_id=self.bpa_id)
        self.otu = mommy.make(OperationalTaxonomicUnit)
        self.sample_otu = mommy.make(SampleOTU, sample=self.BASE_sample, otu=self.otu)

    def testTaxonomicFiltering(self):
        # find SampleContexts with chemical composition boron hot cacl2 = 0.003 with species starting with foobar
        self.otu.species = "foobar baz"
        self.otu.save()
        self.chemical_analysis.boron_hot_cacl2 = 0.003
        self.chemical_analysis.save()

        search_parameters = {"search_field": "boron_hot_cacl2", "search_value": "0.003", "search_species": "foobar*"}
        searcher = Searcher(search_parameters)

        samples = searcher.get_matching_samples()
        assert len(samples) == 1, "Expected one matching sample - got %s" % len(samples)
        found_sample = samples[0]
        assert found_sample.__class__.__name__ == "SampleContext"

    def testRangeSearch(self):
        self.chemical_analysis.boron_hot_cacl2 = 0.5
        self.chemical_analysis.save()

        search_parameters = {"search_range": "boron_hot_cacl2",
                             "search_field": "",
                             "search_range_min": "0.2",
                             "search_range_max": "23.67"
        }

        searcher = Searcher(search_parameters)
        samples = searcher.get_matching_samples()
        assert len(samples) == 1, "Expected one matching sample - got %s" % len(samples)
        found_sample = samples[0]
        assert found_sample.__class__.__name__ == "SampleContext"

    def testSearchOnSiteSubObjectField(self):
        self.collection_site.elevation = 23
        self.collection_site.save()

        search_parameters = {"search_range": "elevation",
                             "search_field": "",
                             "search_range_min": "22",
                             "search_range_max": "24"
        }

        searcher = Searcher(search_parameters)
        samples = searcher.get_matching_samples()
        assert len(samples) == 1, "Expected one matching sample - got %s" % len(samples)
        found_sample = samples[0]
        assert found_sample.__class__.__name__ == "SampleContext"

    def testFailingSearchOnSiteSubObjectField(self):
        self.collection_site.elevation = 25
        self.collection_site.save()

        search_parameters = {"search_range": "elevation",
                             "search_field": "",
                             "search_range_min": "22",
                             "search_range_max": "24"
        }

        searcher = Searcher(search_parameters)
        samples = searcher.get_matching_samples()
        assert len(samples) == 0, "Expected zero matching samples - got %s" % len(samples)









