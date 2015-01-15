from django.test import TestCase
from model_mommy import mommy
# from model_mommy.recipe import Recipe, seq
from ..models import AmpliconSequencingMetadata


class SampleTests(TestCase):
    AMPLICON_SEQUENCING_METADATA_COUNT = 50

    def setUp(self):
        mommy.make(AmpliconSequencingMetadata, _quantity=self.AMPLICON_SEQUENCING_METADATA_COUNT)

    def test_list(self):
        self.assertEquals(len(AmpliconSequencingMetadata.objects.all()), self.AMPLICON_SEQUENCING_METADATA_COUNT)
