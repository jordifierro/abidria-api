from django.test import TestCase

from experiences.entities import Experience
from experiences.models import ORMExperience
from experiences.repositories import ExperienceRepo


class ExperienceRepoTestCase(TestCase):

    def test_get_all_experiences_returns_all_experiences(self):
        orm_exp_a = ORMExperience.objects.create(title='Exp a', description='some description')
        orm_exp_b = ORMExperience.objects.create(title='Exp b', description='other description')

        result = ExperienceRepo().get_all_experiences()

        exp_a = Experience(id=orm_exp_a.id, title='Exp a', description='some description', picture=None)
        exp_b = Experience(id=orm_exp_b.id, title='Exp b', description='other description', picture=None)
        assert result == [exp_a, exp_b]
