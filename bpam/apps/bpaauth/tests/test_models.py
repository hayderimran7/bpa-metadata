from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from ..models import BPAUser

user_recipe = Recipe(
    BPAUser,
    username=seq('bpauser'),
    project='BPA TEST Project',
    organisation='TEST Organisation',
    telephone=seq('99999999_'),
    interest='TEST Interest',
    lab='TESTLAB',
    note='NOTE'
)


class BPAUserTests(TestCase):
    USER_COUNT = 100

    def setUp(self):
        mommy.make(BPAUser, _quantity=self.USER_COUNT)

    def test_list(self):
        self.assertEquals(len(BPAUser.objects.all()), self.USER_COUNT)

    def test_no_user(self):
        self.assertRaises(BPAUser.DoesNotExist, lambda: BPAUser.objects.get(username='testuser666'))

    def test_save_full_user(self):
        user = user_recipe.make()
        user.lab = 'NEW Test lab'
        user.save()
        self.assertIsInstance(BPAUser.objects.get(lab='NEW Test lab'), BPAUser)

    def test_search_user(self):
        user_recipe.make(lab='TESTLAB Impropable')
        self.assertGreater(BPAUser.objects.filter(lab__icontains='testlab impropable'), 0)
