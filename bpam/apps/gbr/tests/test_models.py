import random
import string

from django.test import TestCase
from model_mommy import mommy
from ..models import GBRRun
from ..models import CollectionEvent
from ..models import GBRSample
from ..models import GBRProtocol
from ..models import GBRSequenceFile


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class RunTests(TestCase):
    RUN_COUNT = 10

    def setUp(self):
        mommy.make(GBRRun, _quantity=self.RUN_COUNT)

    def test_list(self):
        self.assertEquals(len(GBRRun.objects.all()), self.RUN_COUNT)


class CollectionEventTest(TestCase):
    RUN_COUNT = 10

    def setUp(self):
        mommy.make(CollectionEvent, _quantity=self.RUN_COUNT)

    def test_list(self):
        self.assertEquals(len(CollectionEvent.objects.all()), self.RUN_COUNT)


class GBRSampleTest(TestCase):
    RUN_COUNT = 10

    def setUp(self):
        mommy.make(GBRSample, _quantity=self.RUN_COUNT)

    def test_list(self):
        self.assertEquals(len(GBRSample.objects.all()), self.RUN_COUNT)


class GBRProtocolTest(TestCase):
    RUN_COUNT = 10

    def setUp(self):
        mommy.make(GBRProtocol, _quantity=self.RUN_COUNT)

    def test_list(self):
        self.assertEquals(len(GBRProtocol.objects.all()), self.RUN_COUNT)


class GBRSequenceFileTest(TestCase):
    RUN_COUNT = 10

    def setUp(self):
        mommy.make(GBRSequenceFile, _quantity=self.RUN_COUNT)

    def test_list(self):
        self.assertEquals(len(GBRSequenceFile.objects.all()), self.RUN_COUNT)
