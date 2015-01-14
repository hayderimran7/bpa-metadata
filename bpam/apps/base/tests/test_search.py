from django.test import TestCase
from model_mommy import mommy

from apps.base.search import Searcher
from apps.base_otu.models import *
from apps.base_contextual.models import *
from apps.base_metagenomics.models import *


class SearchBuilder(object):
    # mocks parameters from the view
    def __init__(self):
        self.parameters = {}
        self.parameters["search_all"] = "No"
        self.parameters["search_terms"] = []
        self.search_all(False)

    def and_search(self):
        self.parameters["search_operator"] = 'and'

    def or_search(self):
        self.parameters["search_operator"] = 'or'

    def search_all(self, search_all=True):
        if search_all:
            self.parameters["search_all"] = "search_all"
        else:
            self.parameters["search_all"] = ""

    def add_search_term(self, field, a, b=None):
        if b is None:
            self.parameters["search_terms"].append((field, str(a)))
        else:
            # range
            self.parameters["search_terms"].append((field, (str(a), str(b))))

    def taxonomy_filter(self, kingdom="", phylum="", klass="", order="", family="", genus="", species=""):
        self.parameters["search_kingdom"] = kingdom
        self.parameters["search_phylum"] = phylum
        self.parameters["search_class"] = klass
        self.parameters["search_order"] = order
        self.parameters["search_family"] = family
        self.parameters["search_genus"] = genus
        self.parameters["search_species"] = species

    def no_taxonomy(self):
        self.taxonomy_filter()


class SearchTestCase(TestCase):
    def _setUpSample(self, name, elevation, boron_hot_cacl2, otu=None):
        bpa_id_name = "bpa_id" + str(name)
        setattr(self, bpa_id_name, mommy.make(BPAUniqueID, bpa_id=str(name)))
        bpa_id = getattr(self, bpa_id_name)
        setattr(self, "collection_site" + str(name), mommy.make(CollectionSite, elevation=elevation))
        site = getattr(self, "collection_site" + str(name))
        setattr(self, "chemical_analysis" + str(name),
                mommy.make(ChemicalAnalysis, bpa_id=bpa_id, boron_hot_cacl2=boron_hot_cacl2))
        setattr(self, "sample_context" + str(name), mommy.make(SampleContext, bpa_id=bpa_id, site=site))
        setattr(self, "metagenomics_sample" + str(name), mommy.make(MetagenomicsSample, bpa_id=bpa_id))
        if otu:
            metagenomics_sample = getattr(self, "metagenomics_sample" + str(name))
            sample_otu_name = "sample_otu" + str(name)
            setattr(self, sample_otu_name, mommy.make(SampleOTU, sample=metagenomics_sample, otu=otu, count=1000))

    def setUp(self):
        super(SearchTestCase, self).setUp()
        # otus
        otu1 = OperationalTaxonomicUnit()
        otu1.name = "otu1"
        otu1.kingdom = "a"
        otu1.phylum = "b"
        otu1.otu_class = "c"
        otu1.order = "d"
        otu1.family = "e"
        otu1.genus = "f"
        otu1.species = "g"
        otu1.save()

        otu2 = OperationalTaxonomicUnit()
        otu2.name = "otu2"
        otu2.kingdom = "a"
        otu2.phylum = "b"
        otu2.otu_class = "c"
        otu2.order = "p"
        otu2.family = "q"
        otu2.genus = "r"
        otu2.species = "s"
        otu2.save()

        otu3 = OperationalTaxonomicUnit()
        otu3.name = "otu3"
        otu3.kingdom = "a"
        otu3.phylum = "b"
        otu3.otu_class = "c"
        otu3.order = "p"
        otu3.family = "q"
        otu3.genus = "t"
        otu3.species = "u"
        otu3.save()

        # sample 1
        self._setUpSample("A", 100, 23.67, otu1)
        # sample 2
        self._setUpSample("B", 100, 67.0, otu2)
        # sample 3
        self._setUpSample("C", 200, 24.67)
        # sample 4
        self._setUpSample("D", 1000, -56.90, otu3)

    def testSimpleSingleSearch(self):
        b = SearchBuilder()
        b.and_search()
        b.add_search_term("elevation", 100)
        b.no_taxonomy()
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 2, "simple single search failed"

    def testSimpleRangeSearch(self):
        b = SearchBuilder()
        b.and_search()
        b.no_taxonomy()
        b.add_search_term("boron_hot_cacl2", 23.0, 25.00)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 2, "simple range search failed"

    def testComplexAndSearch(self):
        b = SearchBuilder()
        b.and_search()
        b.no_taxonomy()
        b.add_search_term("elevation", 100)
        b.add_search_term("boron_hot_cacl2", 67.0)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 1, "complex search and failed"

    def testComplexOrSearch(self):
        b = SearchBuilder()
        b.or_search()
        b.no_taxonomy()
        b.add_search_term("elevation", 100)
        b.add_search_term("boron_hot_cacl2", 24.67)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 3, "complex or search failed"

    def testTaxonomySearchOnAllSamples1(self):
        b = SearchBuilder()
        b.search_all()
        b.and_search()
        b.taxonomy_filter(kingdom="a")
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 3, "taxomic on all failed kingdom"

    def testTaxonomyAndComplexSearch(self):
        b = SearchBuilder()
        b.and_search()
        b.taxonomy_filter(kingdom="a", phylum="b", klass="c")
        b.add_search_term("elevation", 100)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        print results
        assert len(results) == 2, "complex taxomic search failed"

    def testTaxonomyAndComplexSearch2(self):
        b = SearchBuilder()
        b.and_search()
        b.taxonomy_filter(kingdom="a", phylum="b", klass="dfkdjsfdsfj")
        b.add_search_term("elevation", 100)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 0, "complex taxomic search failed"

    def testTaxonomyAndComplexSearch3(self):
        b = SearchBuilder()
        b.and_search()
        b.taxonomy_filter(kingdom="a", phylum="b", klass="c")
        b.add_search_term("boron_hot_cacl2", 23.67)
        searcher = Searcher(b.parameters)
        results = searcher.complex_search()
        assert len(results) == 1, "complex taxomic search failed"