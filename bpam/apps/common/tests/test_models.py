import random
import string

from django.test import TestCase
from model_mommy import mommy
from model_mommy.recipe import Recipe, seq

from ..models import BPAProject
from ..models import BPAUniqueID
from ..models import Organism


project_recipe = Recipe(
    BPAProject,
    name=seq('bpa_project'),
    note='NOTE'
)


def random_string(length=10):
    return u''.join(random.choice(string.ascii_letters) for _ in range(length))


class ProjectTests(TestCase):
    PROJECT_COUNT = 50

    def setUp(self):
        mommy.make(BPAProject, _quantity=self.PROJECT_COUNT)

    def test_list(self):
        self.assertEquals(len(BPAProject.objects.all()), self.PROJECT_COUNT)

    def test_no_user(self):
        self.assertRaises(BPAProject.DoesNotExist, lambda: BPAProject.objects.get(name='herpderp666'))

    def test_save_project(self):
        name = 'TEST PROJECT XXX'
        project = project_recipe.make()
        project.name = name
        project.save()
        self.assertIsInstance(BPAProject.objects.get(name=name), BPAProject)

    def test_search_project(self):
        project_recipe.make(name='Project Impropable')
        self.assertGreater(BPAProject.objects.filter(name__icontains='impropable'), 0)

    def test_description_size(self):
        size = 2000
        project = project_recipe.make()
        project.description = random_string(size)
        project.save()
        self.assertEqual(len(project.description), size)


class BPAUniqueIDTests(TestCase):
    ID_COUNT = 100

    def setUp(self):
        mommy.make(BPAUniqueID, _quantity=self.ID_COUNT)

    def test_list(self):
        self.assertEquals(len(BPAUniqueID.objects.all()), self.ID_COUNT)


class OrganismTests(TestCase):

    def test_organism_name(self):
        organism = mommy.make(Organism, genus='GGGG', species='SSSS')
        self.assertEqual(str(organism), 'GGGG SSSS')








