from django.test import TestCase

from abidria.exceptions import EntityDoesNotExistException
from experiences.entities import Experience
from experiences.models import ORMExperience
from experiences.repositories import ExperienceRepo
from people.models import ORMPerson


class ExperienceRepoTestCase(TestCase):

    def test_get_all_experiences_with_mine_false(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_created_by_first_person_in_db() \
                .given_another_experience_created_by_first_person_in_db() \
                .given_another_person_in_db() \
                .given_an_experience_created_by_second_person_in_db() \
                .given_another_experience_created_by_second_person_in_db() \
                .given_logged_person_id_is_first_person_id() \
                .when_get_all_experiences(mine=False) \
                .then_repo_should_return_just_second_two_experience()

    def test_get_all_experiences_with_mine_true(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_created_by_first_person_in_db() \
                .given_another_experience_created_by_first_person_in_db() \
                .given_another_person_in_db() \
                .given_an_experience_created_by_second_person_in_db() \
                .given_another_experience_created_by_second_person_in_db() \
                .given_logged_person_id_is_first_person_id() \
                .when_get_all_experiences(mine=True) \
                .then_repo_should_return_just_first_two_experience()

    def test_get_experience_returns_experience(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .when_get_experience_with_its_id() \
                .then_repo_should_return_experience()

    def test_get_unexistent_experience_raises_error(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .when_get_unexistent_experience() \
                .then_entity_does_not_exists_should_be_raised()

    def test_create_experience_creates_and_returns_experience(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_to_create() \
                .when_create_this_experience() \
                .then_should_return_this_experience() \
                .then_should_save_this_experience_to_db()

    def test_update_experience(self):
        ExperienceRepoTestCase._ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .given_an_updated_experience() \
                .when_update_first_experience() \
                .then_result_should_be_same_as_updated() \
                .then_updated_experience_should_be_saved_on_db()

    class _ScenarioMaker(object):

        def __init__(self):
            self._orm_person = None
            self._orm_experience_a = None
            self._orm_experience_b = None
            self._experience_a = None
            self._experience_b = None
            self._result = None
            self._entity_does_not_exist_error = None
            self._experience_to_create = None

        def given_a_person_in_db(self):
            self._orm_person = ORMPerson.objects.create(username='usr')
            return self

        def given_another_person_in_db(self):
            self._second_orm_person = ORMPerson.objects.create(username='nme')
            return self

        def given_an_experience_created_by_first_person_in_db(self):
            self._orm_experience_a = ORMExperience.objects.create(title='Exp a', description='some description',
                                                                  author=self._orm_person)
            self._experience_a = Experience(id=self._orm_experience_a.id, title='Exp a', description='some description',
                                            author_id=self._orm_person.id, author_username=self._orm_person.username)
            return self

        def given_another_experience_created_by_first_person_in_db(self):
            self._orm_experience_b = ORMExperience.objects.create(title='Exp b', description='some description',
                                                                  author=self._orm_person)
            self._experience_b = Experience(id=self._orm_experience_b.id, title='Exp b', description='some description',
                                            author_id=self._orm_person.id, author_username=self._orm_person.username)
            return self

        def given_an_experience_created_by_second_person_in_db(self):
            self._orm_experience_c = ORMExperience.objects.create(title='Exp c', description='description',
                                                                  author=self._second_orm_person)
            self._experience_c = Experience(id=self._orm_experience_c.id, title='Exp c', description='description',
                                            author_id=self._second_orm_person.id,
                                            author_username=self._second_orm_person.username)
            return self

        def given_another_experience_created_by_second_person_in_db(self):
            self._orm_experience_d = ORMExperience.objects.create(title='Exp d', description='description',
                                                                  author=self._second_orm_person)
            self._experience_d = Experience(id=self._orm_experience_d.id, title='Exp d', description='description',
                                            author_id=self._second_orm_person.id,
                                            author_username=self._second_orm_person.username)
            return self

        def given_logged_person_id_is_first_person_id(self):
            self.logged_person_id = self._orm_person.id
            return self

        def given_an_experience_to_create(self):
            self._experience_to_create = Experience(id="", title='Exp a', description='some description',
                                                    author_id=self._orm_person.id)
            return self

        def given_an_experience_in_db(self):
            self._orm_experience_a = ORMExperience.objects.create(title='Exp a', description='some description',
                                                                  author=self._orm_person)
            self._experience_a = Experience(id=self._orm_experience_a.id, title='Exp a', description='some description',
                                            author_id=self._orm_person.id, author_username=self._orm_person.username)
            return self

        def given_an_updated_experience(self):
            self._updated_experience = Experience(id=self._experience_a.id, title='T2', description='updated',
                                                  author_id=self._orm_person.id,
                                                  author_username=self._orm_person.username)
            return self

        def given_another_experience_in_db(self):
            self._orm_experience_b = ORMExperience.objects.create(title='Exp b', description='other description',
                                                                  author=self._orm_person)
            self._experience_b = Experience(id=self._orm_experience_b.id, title='Exp b',
                                            description='other description',
                                            author_id=self._orm_person.id, author_username=self._orm_person.username)
            return self

        def when_get_all_experiences(self, mine):
            self._result = ExperienceRepo().get_all_experiences(logged_person_id=self.logged_person_id, mine=mine)
            return self

        def when_get_experience_with_its_id(self):
            self._result = ExperienceRepo().get_experience(self._orm_experience_a.id)
            return self

        def when_get_unexistent_experience(self):
            try:
                ExperienceRepo().get_experience(0)
            except EntityDoesNotExistException as e:
                self._entity_does_not_exist_error = e
            return self

        def when_create_this_experience(self):
            self._result = ExperienceRepo().create_experience(self._experience_to_create)
            return self

        def when_update_first_experience(self):
            self._result = ExperienceRepo().update_experience(self._updated_experience)
            return self

        def then_repo_should_return_just_first_two_experience(self):
            assert self._result == [self._experience_b, self._experience_a]
            return self

        def then_repo_should_return_just_second_two_experience(self):
            assert self._result == [self._experience_c, self._experience_d]
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

        def then_result_should_be_same_as_updated(self):
            assert self._updated_experience.title == self._result.title
            assert self._updated_experience.description == self._result.description
            assert not self._result.picture
            return self

        def then_updated_experience_should_be_saved_on_db(self):
            orm_experience = ORMExperience.objects.get(id=self._result.id,
                                                       title=self._updated_experience.title,
                                                       description=self._updated_experience.description)
            assert orm_experience is not None
            return self
