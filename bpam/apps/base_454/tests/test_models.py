from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import Sample454


class SampleTests(TestCase):
    _COUNT = 50

    def setUp(self):
        mommy.make(Sample454, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(Sample454.objects.all()), self._COUNT)
