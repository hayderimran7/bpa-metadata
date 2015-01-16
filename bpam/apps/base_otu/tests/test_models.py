from django.test import TestCase
from model_mommy import mommy
from ..models import OperationalTaxonomicUnit
from ..models import SampleOTU


class OTUTests(TestCase):
    _COUNT = 1000

    def setUp(self):
        mommy.make(OperationalTaxonomicUnit, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(OperationalTaxonomicUnit.objects.all()), self._COUNT)


class SampleOTUTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(SampleOTU, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(SampleOTU.objects.all()), self._COUNT)
