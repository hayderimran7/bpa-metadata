from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import WheatPathogenTranscriptProtocol
from ..models import WheatPathogenTranscriptRun
from ..models import WheatPathogenTranscriptSample
from ..models import WheatPathogenTranscriptSequenceFile


class WheatPathogenTranscriptProtocolTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(WheatPathogenTranscriptProtocol, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(WheatPathogenTranscriptProtocol.objects.all()), self._COUNT)


class WheatPathogenTranscriptSampleTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(WheatPathogenTranscriptSample, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(WheatPathogenTranscriptSample.objects.all()), self._COUNT)


class WheatPathogenTranscriptRunTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(WheatPathogenTranscriptRun, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(WheatPathogenTranscriptRun.objects.all()), self._COUNT)


class WheatPathogenTranscriptSequenceFileTests(TestCase):
    _COUNT = 10

    def setUp(self):
        mommy.make(WheatPathogenTranscriptSequenceFile, _quantity=self._COUNT)

    def test_list(self):
        self.assertEquals(len(WheatPathogenTranscriptSequenceFile.objects.all()), self._COUNT)
