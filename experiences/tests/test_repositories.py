from django.test import TestCase

from abidria.exceptions import EntityDoesNotExistException
from experiences.entities import Experience
from experiences.models import ORMExperience, ORMSave
from experiences.repositories import ExperienceRepo
from people.models import ORMPerson


class ExperienceRepoTestCase(TestCase):

    def test_get_all_experiences_with_mine_false(self):
        ExperienceRepoTestCase.ScenarioMaker() \
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
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_created_by_first_person_in_db() \
                .given_another_experience_created_by_first_person_in_db() \
                .given_another_person_in_db() \
                .given_an_experience_created_by_second_person_in_db() \
                .given_another_experience_created_by_second_person_in_db() \
                .given_logged_person_id_is_first_person_id() \
                .when_get_all_experiences(mine=True) \
                .then_repo_should_return_just_first_two_experience()

    def test_get_all_experiences_with_saved_true(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_created_by_first_person_in_db() \
                .given_another_experience_created_by_first_person_in_db() \
                .given_another_person_in_db() \
                .given_an_experience_created_by_second_person_in_db() \
                .given_another_experience_created_by_second_person_in_db() \
                .given_a_save_to_first_second_person_experience_from_first_person() \
                .given_logged_person_id_is_first_person_id() \
                .when_get_all_experiences(saved=True) \
                .then_repo_should_return_just_first_second_person_experience()

    def test_get_experience_returns_experience(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .when_get_experience_with_its_id() \
                .then_repo_should_return_experience()

    def test_get_unexistent_experience_raises_error(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .when_get_unexistent_experience() \
                .then_entity_does_not_exists_should_be_raised()

    def test_create_experience_creates_and_returns_experience(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_to_create() \
                .when_create_this_experience() \
                .then_should_return_this_experience() \
                .then_should_save_this_experience_to_db()

    def test_update_experience(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .given_an_updated_experience() \
                .when_update_first_experience() \
                .then_result_should_be_same_as_updated() \
                .then_updated_experience_should_be_saved_on_db()

    def test_save_experience(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .when_save_that_experience() \
                .then_result_should_be_true() \
                .then_save_should_be_created_for_that_experience_and_person()

    def test_save_twice_doesnt_create_2_saves(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .given_a_save_for_that_person_and_experience() \
                .when_save_that_experience() \
                .then_result_should_be_true() \
                .then_save_for_that_experience_and_person_should_be_only_one()

    def test_unsave_experience(self):
        ExperienceRepoTestCase.ScenarioMaker() \
                .given_a_person_in_db() \
                .given_an_experience_in_db() \
                .given_a_save_for_that_person_and_experience() \
                .when_unsave_that_experience() \
                .then_result_should_be_true() \
                .then_save_should_be_deleted_from_db()

    class ScenarioMaker(object):

        def __init__(self):
            self.orm_person = None
            self.orm_experience_a = None
            self.orm_experience_b = None
            self.experience_a = None
            self.experience_b = None
            self.result = None
            self.entity_does_not_exist_error = None
            self.experience_to_create = None

        def given_a_person_in_db(self):
            self.orm_person = ORMPerson.objects.create(username='usr')
            return self

        def given_another_person_in_db(self):
            self.second_orm_person = ORMPerson.objects.create(username='nme')
            return self

        def given_an_experience_created_by_first_person_in_db(self):
            self.orm_experience_a = ORMExperience.objects.create(title='Exp a', description='some description',
                                                                 author=self.orm_person)
            self.experience_a = Experience(id=self.orm_experience_a.id, title='Exp a', description='some description',
                                           author_id=self.orm_person.id, author_username=self.orm_person.username)
            return self

        def given_another_experience_created_by_first_person_in_db(self):
            self.orm_experience_b = ORMExperience.objects.create(title='Exp b', description='some description',
                                                                 author=self.orm_person)
            self.experience_b = Experience(id=self.orm_experience_b.id, title='Exp b', description='some description',
                                           author_id=self.orm_person.id, author_username=self.orm_person.username)
            return self

        def given_an_experience_created_by_second_person_in_db(self):
            self.orm_experience_c = ORMExperience.objects.create(title='Exp c', description='description',
                                                                 author=self.second_orm_person)
            self.experience_c = Experience(id=self.orm_experience_c.id, title='Exp c', description='description',
                                           author_id=self.second_orm_person.id,
                                           author_username=self.second_orm_person.username)
            return self

        def given_another_experience_created_by_second_person_in_db(self):
            self.orm_experience_d = ORMExperience.objects.create(title='Exp d', description='description',
                                                                 author=self.second_orm_person)
            self.experience_d = Experience(id=self.orm_experience_d.id, title='Exp d', description='description',
                                           author_id=self.second_orm_person.id,
                                           author_username=self.second_orm_person.username)
            return self

        def given_logged_person_id_is_first_person_id(self):
            self.logged_person_id = self.orm_person.id
            return self

        def given_an_experience_to_create(self):
            self.experience_to_create = Experience(id="", title='Exp a', description='some description',
                                                   author_id=self.orm_person.id)
            return self

        def given_an_experience_in_db(self):
            self.orm_experience_a = ORMExperience.objects.create(title='Exp a', description='some description',
                                                                 author=self.orm_person)
            self.experience_a = Experience(id=self.orm_experience_a.id, title='Exp a', description='some description',
                                           author_id=self.orm_person.id, author_username=self.orm_person.username)
            return self

        def given_an_updated_experience(self):
            self.updated_experience = Experience(id=self.experience_a.id, title='T2', description='updated',
                                                 author_id=self.orm_person.id,
                                                 author_username=self.orm_person.username)
            return self

        def given_another_experience_in_db(self):
            self.orm_experience_b = ORMExperience.objects.create(title='Exp b', description='other description',
                                                                 author=self.orm_person)
            self.experience_b = Experience(id=self.orm_experience_b.id, title='Exp b',
                                           description='other description',
                                           author_id=self.orm_person.id, author_username=self.orm_person.username)
            return self

        def given_a_save_for_that_person_and_experience(self):
            ORMSave.objects.create(person=self.orm_person, experience=self.orm_experience_a)
            return self

        def given_a_save_to_first_second_person_experience_from_first_person(self):
            ORMSave.objects.create(person=self.orm_person, experience=self.orm_experience_c)
            return self

        def when_get_all_experiences(self, mine=False, saved=False):
            self.result = ExperienceRepo().get_all_experiences(logged_person_id=self.logged_person_id,
                                                               mine=mine, saved=saved)
            return self

        def when_get_experience_with_its_id(self):
            self.result = ExperienceRepo().get_experience(self.orm_experience_a.id)
            return self

        def when_get_unexistent_experience(self):
            try:
                ExperienceRepo().get_experience(0)
            except EntityDoesNotExistException as e:
                self.entity_does_not_exist_error = e
            return self

        def when_create_this_experience(self):
            self.result = ExperienceRepo().create_experience(self.experience_to_create)
            return self

        def when_update_first_experience(self):
            self.result = ExperienceRepo().update_experience(self.updated_experience)
            return self

        def when_save_that_experience(self):
            try:
                self.result = ExperienceRepo().save_experience(person_id=self.orm_person.id,
                                                               experience_id=self.orm_experience_a.id)
            except Exception as e:
                self.error = e
            return self

        def when_unsave_that_experience(self):
            try:
                self.result = ExperienceRepo().unsave_experience(person_id=self.orm_person.id,
                                                                 experience_id=self.orm_experience_a.id)
            except Exception as e:
                self.error = e
            return self

        def then_repo_should_return_just_first_two_experience(self):
            assert self.result == [self.experience_b, self.experience_a]
            return self

        def then_repo_should_return_just_second_two_experience(self):
            assert self.result == [self.experience_c, self.experience_d]
            return self

        def then_repo_should_return_just_first_second_person_experience(self):
            assert self.result == [self.experience_c]
            return self

        def then_repo_should_return_experience(self):
            assert self.result == self.experience_a
            return self

        def then_entity_does_not_exists_should_be_raised(self):
            assert self.entity_does_not_exist_error is not None
            return self

        def then_should_return_this_experience(self):
            assert self.result.title == self.experience_to_create.title
            assert self.result.description == self.experience_to_create.description
            return self

        def then_should_save_this_experience_to_db(self):
            exp = ExperienceRepo().get_experience(self.result.id)
            assert exp.title == self.experience_to_create.title
            assert exp.description == self.experience_to_create.description
            return self

        def then_result_should_be_same_as_updated(self):
            assert self.updated_experience.title == self.result.title
            assert self.updated_experience.description == self.result.description
            assert not self.result.picture
            return self

        def then_updated_experience_should_be_saved_on_db(self):
            orm_experience = ORMExperience.objects.get(id=self.result.id,
                                                       title=self.updated_experience.title,
                                                       description=self.updated_experience.description)
            assert orm_experience is not None
            return self

        def then_result_should_be_true(self):
            assert self.result is True
            return self

        def then_save_should_be_created_for_that_experience_and_person(self):
            assert ORMSave.objects.filter(person=self.orm_person, experience=self.orm_experience_a).exists()
            return self

        def then_save_for_that_experience_and_person_should_be_only_one(self):
            assert len(ORMSave.objects.filter(person=self.orm_person, experience=self.orm_experience_a)) == 1
            return self

        def then_save_should_be_deleted_from_db(self):
            assert not ORMSave.objects.filter(person=self.orm_person, experience=self.orm_experience_a).exists()
            return self
