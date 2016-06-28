import random
import string

from django.test import TestCase
from model_mommy import mommy
from ..models import (TumorStage, Array, MelanomaSample, MelanomaRun, MelanomaProtocol, MelanomaSequenceFile)


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class TumorStageTests(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(TumorStage, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(TumorStage.objects.all()), self.ID_COUNT)


class ArrayTests(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(Array, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(Array.objects.all()), self.ID_COUNT)


class MelanomaSampleTests(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(MelanomaSample, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(MelanomaSample.objects.all()), self.ID_COUNT)


class MelanomaRunTest(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(MelanomaRun, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(MelanomaRun.objects.all()), self.ID_COUNT)


class MelanomaProtocolTest(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(MelanomaProtocol, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(MelanomaProtocol.objects.all()), self.ID_COUNT)


class MelanomaSequenceFileTest(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(MelanomaSequenceFile, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(MelanomaSequenceFile.objects.all()), self.ID_COUNT)
