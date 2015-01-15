from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import MetagenomicsSample
from ..models import MetagenomicsRun
from ..models import MetagenomicsSequenceFile


class SampleTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(MetagenomicsSample, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(MetagenomicsSample.objects.all()), self._COUNT)


class MetagenomicsRunTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(MetagenomicsRun, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(MetagenomicsRun.objects.all()), self._COUNT)


class MetagenomicsSequenceFileTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(MetagenomicsSequenceFile, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(MetagenomicsSequenceFile.objects.all()), self._COUNT)
