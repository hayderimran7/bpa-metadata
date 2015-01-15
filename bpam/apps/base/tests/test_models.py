from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import BASESample


class SampleTests(TestCase):
    _COUNT = 50

    def setUp(self):
        mommy.make(BASESample, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(BASESample.objects.all()), self._COUNT)
