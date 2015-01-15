from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import PathogenSample
from ..models import PathogenProtocol
from ..models import PathogenRun
from ..models import PathogenSequenceFile


class PathogenProtocolTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(PathogenProtocol, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(PathogenProtocol.objects.all()), self._COUNT)


class PathogenSampleTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(PathogenSample, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(PathogenSample.objects.all()), self._COUNT)


class PathogenRunTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(PathogenRun, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(PathogenRun.objects.all()), self._COUNT)


class PathogenSequenceFileTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(PathogenSequenceFile, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(PathogenSequenceFile.objects.all()), self._COUNT)
