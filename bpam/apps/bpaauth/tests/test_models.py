from django.test import TestCase
from ..models import BPAUser


class BPAUserTests(TestCase):
    USER_COUNT = 100

    def setUp(self):
        for i in range(self.USER_COUNT):
            username = 'testuser' + str(i)
            BPAUser.objects.get_or_create(username=username)

    def test_list(self):
        self.assertEquals(len(BPAUser.objects.all()), self.USER_COUNT)

    def test_no_user(self):
        self.assertRaises(BPAUser.DoesNotExist, lambda: BPAUser.objects.get(username='testuser666'))
