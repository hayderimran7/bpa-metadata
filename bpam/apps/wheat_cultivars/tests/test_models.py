from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import CultivarProtocol
from ..models import CultivarRun
from ..models import CultivarSample
from ..models import CultivarSequenceFile


class CultivarProtocolTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(CultivarProtocol, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(CultivarProtocol.objects.all()), self._COUNT)


class CultivarRunTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(CultivarRun, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(CultivarRun.objects.all()), self._COUNT)


class CultivarSampleTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(CultivarSample, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(CultivarSample.objects.all()), self._COUNT)


class CultivarSequenceFileTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(CultivarSequenceFile, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(CultivarSequenceFile.objects.all()), self._COUNT)
