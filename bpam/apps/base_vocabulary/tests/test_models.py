from django.test import TestCase
from model_mommy import mommy
from ..models import LandUse


class LandUseTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(LandUse, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(LandUse.objects.all()), self._COUNT)
