from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import CollectionSite
from ..models import ChemicalAnalysis
from ..models import SampleContext


class CollectionSiteTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(CollectionSite, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(CollectionSite.objects.all()), self._COUNT)


class ChemicalAnalysisTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(ChemicalAnalysis, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(ChemicalAnalysis.objects.all()), self._COUNT)


class SampleContextTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(SampleContext, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(SampleContext.objects.all()), self._COUNT)
