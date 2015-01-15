from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import LandUse
from ..models import SoilTexture


class LandUseTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(LandUse, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(LandUse.objects.all()), self._COUNT)


class SoilTextureTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(SoilTexture, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(SoilTexture.objects.all()), self._COUNT)


