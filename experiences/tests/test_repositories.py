from django.test import TestCase

from abidria.exceptions import EntityDoesNotExist
from experiences.entities import Experience
from experiences.models import ORMExperience
from experiences.repositories import ExperienceRepo


class ExperienceRepoTestCase(TestCase):

    def test_get_all_experiences_returns_all_experiences(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_an_experience_in_db() \
                .given_another_experience_in_db() \
                .when_get_all_experiences() \
                .then_repo_should_return_both_experiences()

    def test_get_experience_returns_experience(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_an_experience_in_db() \
                .when_get_experience_with_its_id() \
                .then_repo_should_return_experience()

    def test_get_unexistent_experience_raises_error(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .when_get_unexistent_experience() \
                .then_entity_does_not_exists_should_be_raised()

    def test_create_experience_creates_and_returns_experience(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_an_experience_to_create() \
                .when_create_this_experience() \
                .then_should_return_this_experience() \
                .then_should_save_this_experience_to_db()

    class _ScenarioMaker(object):

        def __init__(self):
            self._orm_experience_a = None
            self._orm_experience_b = None
            self._experience_a = None
            self._experience_b = None
            self._result = None
            self._entity_does_not_exist_error = None
            self._experience_to_create = None

        def given_an_experience_to_create(self):
            self._experience_to_create = Experience(id="", title='Exp a', description='some description')
            return self

        def given_an_experience_in_db(self):
            self._orm_experience_a = ORMExperience.objects.create(title='Exp a',
                                                                  description='some description')
            self._experience_a = Experience(id=self._orm_experience_a.id, title='Exp a',
                                            description='some description')
            return self

        def given_another_experience_in_db(self):
            self._orm_experience_b = ORMExperience.objects.create(title='Exp b',
                                                                  description='other description')
            self._experience_b = Experience(id=self._orm_experience_b.id, title='Exp b',
                                            description='other description')
            return self

        def when_get_all_experiences(self):
            self._result = ExperienceRepo().get_all_experiences()
            return self

        def when_get_experience_with_its_id(self):
            self._result = ExperienceRepo().get_experience(self._orm_experience_a.id)
            return self

        def when_get_unexistent_experience(self):
            try:
                ExperienceRepo().get_experience(0)
            except EntityDoesNotExist as e:
                self._entity_does_not_exist_error = e
            return self

        def when_create_this_experience(self):
            self._result = ExperienceRepo().create_experience(self._experience_to_create)
            return self

        def then_repo_should_return_both_experiences(self):
            assert self._result == [self._experience_a, self._experience_b]
            return self

        def then_repo_should_return_experience(self):
            assert self._result == self._experience_a
            return self

        def then_entity_does_not_exists_should_be_raised(self):
            assert self._entity_does_not_exist_error is not None
            return self

        def then_should_return_this_experience(self):
            assert self._result.title == self._experience_to_create.title
            assert self._result.description == self._experience_to_create.description
            return self

        def then_should_save_this_experience_to_db(self):
            exp = ExperienceRepo().get_experience(self._result.id)
            assert exp.title == self._experience_to_create.title
            assert exp.description == self._experience_to_create.description
            return self
