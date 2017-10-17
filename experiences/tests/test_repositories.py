from django.test import TestCase

from abidria.exceptions import EntityDoesNotExist
from experiences.entities import Experience
from experiences.models import ORMExperience
from experiences.repositories import ExperienceRepo


class ExperienceRepoTestCase(TestCase):

    def test_get_all_experiences_returns_all_experiences(self):
        orm_exp_a = ORMExperience.objects.create(title='Exp a', description='some description')
        orm_exp_b = ORMExperience.objects.create(title='Exp b', description='other description')

        result = ExperienceRepo().get_all_experiences()

        exp_a = Experience(id=orm_exp_a.id, title='Exp a', description='some description')
        exp_b = Experience(id=orm_exp_b.id, title='Exp b', description='other description')
        assert result == [exp_a, exp_b]

    def test_get_experience_returns_experience(self):
        orm_exp = ORMExperience.objects.create(title='Exp', description='some description')

        result = ExperienceRepo().get_experience(orm_exp.id)

        assert result == Experience(id=orm_exp.id, title='Exp', description='some description')

    def test_get_unexistent_experience_raises_error(self):
        try:
            ExperienceRepo().get_experience(0)
            assert False
        except EntityDoesNotExist:
            pass
