from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException
from experiences.entities import Experience
from experiences.interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor, \
        ModifyExperienceInteractor


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        TestGetAllExperiences.ScenarioMaker() \
                .given_an_experience() \
                .given_another_experience() \
                .given_a_repo_that_returns_both_experiences() \
                .when_interactor_is_executed() \
                .then_result_should_be_both_experiences()

    class ScenarioMaker(object):

        def given_an_experience(self):
            self.experience_a = Experience(id=1, title='A', description='some',
                                           picture=None, author_id='1', author_username='usr')
            return self

        def given_another_experience(self):
            self.experience_b = Experience(id=2, title='B', description='other',
                                           picture=None, author_id='1', author_username='usr')
            return self

        def given_a_repo_that_returns_both_experiences(self):
            self.experiences_repo = Mock()
            self.experiences_repo.get_all_experiences.return_value = [self.experience_a, self.experience_b]
            return self

        def when_interactor_is_executed(self):
            self.response = GetAllExperiencesInteractor(self.experiences_repo).execute()
            return self

        def then_result_should_be_both_experiences(self):
            assert self.response == [self.experience_a, self.experience_b]
            return self


class TestCreateNewExperience(object):

    def test_creates_and_returns_experience(self):
        TestCreateNewExperience.ScenarioMaker() \
                .given_an_experience() \
                .given_an_experience_repo_that_returns_that_experience_on_create() \
                .given_a_title() \
                .given_a_description() \
                .given_an_author_id() \
                .given_an_experience_validator_that_accepts_them() \
                .when_execute_interactor() \
                .then_result_should_be_the_experience() \
                .then_repo_create_method_should_be_called_with_params() \
                .then_params_should_be_validated()

    def test_invalid_experience_returns_error_and_doesnt_create_it(self):
        TestCreateNewExperience.ScenarioMaker() \
                .given_an_experience() \
                .given_an_experience_repo() \
                .given_a_title() \
                .given_a_description() \
                .given_an_author_id() \
                .given_an_experience_validator_that_raises_invalid_entity_exception() \
                .when_execute_interactor() \
                .then_should_raise_invalid_entity_exception() \
                .then_params_should_be_validated() \
                .then_repo_create_method_should_not_be_called()

    class ScenarioMaker(object):

        def given_an_experience(self):
            self.experience = Experience(title='Title', description='', author_id='3')
            return self

        def given_an_experience_repo_that_returns_that_experience_on_create(self):
            self.experience_repo = Mock()
            self.experience_repo.create_experience.return_value = self.experience
            return self

        def given_a_title(self):
            self.title = 'Title'
            return self

        def given_a_description(self):
            self.description = 'desc'
            return self

        def given_an_author_id(self):
            self.author_id = '4'
            return self

        def given_an_experience_repo(self):
            self.experience_repo = Mock()
            return self

        def given_an_experience_validator_that_accepts_them(self):
            self.experience_validator = Mock()
            self.experience_validator.validate_experience.return_value = True
            return self

        def given_an_experience_validator_that_raises_invalid_entity_exception(self):
            self.experience_validator = Mock()
            self.experience_validator.validate_experience.side_effect = \
                InvalidEntityException(source='title', code='empty_attribute',
                                       message='Title must be between 1 and 20 chars')
            return self

        def when_execute_interactor(self):
            try:
                self.response = CreateNewExperienceInteractor(self.experience_repo, self.experience_validator) \
                    .set_params(title=self.title, description=self.description,
                                logged_person_id=self.author_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_result_should_be_the_experience(self):
            assert self.response == self.experience
            return self

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'title'
            assert self.error.code == 'empty_attribute'
            assert str(self.error) == 'Title must be between 1 and 20 chars'
            return self

        def then_repo_create_method_should_be_called_with_params(self):
            experience_params = Experience(title=self.title, description=self.description, author_id=self.author_id)
            self.experience_repo.create_experience.assert_called_once_with(experience_params)
            return self

        def then_repo_create_method_should_not_be_called(self):
            self.experience_repo.create_experience.assert_not_called()
            return self

        def then_params_should_be_validated(self):
            experience_params = Experience(title=self.title, description=self.description, author_id=self.author_id)
            self.experience_validator.validate_experience.assert_called_once_with(experience_params)
            return self


class TestModifyExperience(object):

    def test_gets_modifies_not_none_params_and_returns_experience(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_experience() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_another_experience_updated_with_that_params() \
                .given_an_experience_repo_that_returns_both_experiences_on_get_and_update() \
                .given_an_experience_validator_that_accepts() \
                .when_interactor_is_executed() \
                .then_result_should_be_second_experience() \
                .then_get_experience_should_be_called_with_id() \
                .then_experience_validation_should_be_called_with_updated_experience() \
                .then_update_experience_should_be_called_with_updated_experience()

    def test_invalid_experience_returns_error_and_doesnt_update_it(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_an_experience() \
                .given_another_experience_updated_with_that_params() \
                .given_an_experience_repo_that_returns_that_experience_on_get() \
                .given_an_experience_validator_that_raises_invalid_entity_exception() \
                .when_interactor_is_executed() \
                .then_should_raise_invalid_entity_exception() \
                .then_get_experience_should_be_called_with_id() \
                .then_experience_validation_should_be_called_with_updated_experience() \
                .then_update_experience_should_be_not_called()

    def test_unexistent_experience_returns_entity_does_not_exist_error(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_an_experience_repo_that_raises_entity_does_not_exist() \
                .given_an_experience_validator() \
                .when_interactor_is_executed() \
                .then_should_raise_entity_does_not_exists() \
                .then_get_experience_should_be_called_with_id() \
                .then_update_experience_should_be_not_called()

    class ScenarioMaker(object):

        def given_an_experience(self):
            self.experience = Experience(id='1', title='Title', description='some',
                                         author_id='2', author_username='usr')
            return self

        def given_an_id(self):
            self.id = '1'
            return self

        def given_a_description(self):
            self.description = ''
            return self

        def given_a_logged_person_id(self):
            self.logged_person_id = '2'
            return self

        def given_another_experience_updated_with_that_params(self):
            self.updated_experience = Experience(id=self.experience.id, title=self.experience.title,
                                                 description=self.description, author_id=self.experience.author_id)
            return self

        def given_an_experience_repo_that_returns_both_experiences_on_get_and_update(self):
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = self.experience
            self.experience_repo.update_experience.return_value = self.updated_experience
            return self

        def given_an_experience_repo_that_returns_that_experience_on_get(self):
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = self.experience
            return self

        def given_an_experience_repo_that_raises_entity_does_not_exist(self):
            self.experience_repo = Mock()
            self.experience_repo.get_experience.side_effect = EntityDoesNotExistException()
            return self

        def given_an_experience_validator(self):
            self.experience_validator = Mock()
            return self

        def given_an_experience_validator_that_accepts(self):
            self.experience_validator = Mock()
            self.experience_validator.validate_experience.return_value = True
            return self

        def given_an_experience_validator_that_raises_invalid_entity_exception(self):
            self.experience_validator = Mock()
            self.experience_validator.validate_experience.side_effect = \
                InvalidEntityException(source='title', code='empty_attribute',
                                       message='Title must be between 1 and 20 chars')
            return self

        def when_interactor_is_executed(self):
            try:
                self.result = ModifyExperienceInteractor(self.experience_repo, self.experience_validator) \
                    .set_params(id=self.id, title=None, description=self.description,
                                logged_person_id=self.logged_person_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_result_should_be_second_experience(self):
            assert self.result == self.updated_experience
            return self

        def then_get_experience_should_be_called_with_id(self):
            self.experience_repo.get_experience.assert_called_once_with(id=self.id)
            return self

        def then_experience_validation_should_be_called_with_updated_experience(self):
            self.experience_validator.validate_experience.assert_called_once_with(self.updated_experience)
            return self

        def then_update_experience_should_be_called_with_updated_experience(self):
            self.experience_validator.validate_experience.assert_called_once_with(self.updated_experience)
            return self

        def then_update_experience_should_be_not_called(self):
            self.experience_repo.updated_experience.assert_not_called()
            return self

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'title'
            assert self.error.code == 'empty_attribute'
            assert str(self.error) == 'Title must be between 1 and 20 chars'
            return self

        def then_should_raise_entity_does_not_exists(self):
            assert type(self.error) is EntityDoesNotExistException
            return self
