from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException, NoLoggedException, \
        NoPermissionException, ConflictException
from experiences.entities import Experience
from experiences.interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor, \
        ModifyExperienceInteractor, UploadExperiencePictureInteractor, SaveUnsaveExperienceInteractor


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        TestGetAllExperiences.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_mine_true() \
                .given_saved_true() \
                .given_a_permission_validator_that_returns_true() \
                .given_an_experience() \
                .given_another_experience() \
                .given_a_repo_that_returns_both_experiences() \
                .when_interactor_is_executed() \
                .then_validate_permissions_should_be_called_with_logged_person_id() \
                .then_result_should_be_both_experiences()

    def test_no_logged_raises_exception(self):
        TestGetAllExperiences.ScenarioMaker() \
                .given_a_permission_validator_that_raises_exception() \
                .when_interactor_is_executed() \
                .then_validate_permissions_should_be_called_with_logged_person_id() \
                .then_should_raise_no_logged_exception()

    class ScenarioMaker(object):

        def __init__(self):
            self.logged_person_id = None
            self.experience_repo = None
            self.permissions_validator = None
            self.mine = None
            self.saved = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '0'
            return self

        def given_mine_true(self):
            self.mine = True
            return self

        def given_saved_true(self):
            self.saved = True
            return self

        def given_an_experience(self):
            self.experience_a = Experience(id=1, title='A', description='some',
                                           picture=None, author_id='1', author_username='usr')
            return self

        def given_another_experience(self):
            self.experience_b = Experience(id=2, title='B', description='other',
                                           picture=None, author_id='1', author_username='usr')
            return self

        def given_a_permission_validator_that_returns_true(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.return_value = True
            return self

        def given_a_permission_validator_that_raises_exception(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.side_effect = NoLoggedException()
            return self

        def given_a_repo_that_returns_both_experiences(self):
            self.experience_repo = Mock()
            self.experience_repo.get_all_experiences.return_value = [self.experience_a, self.experience_b]
            return self

        def when_interactor_is_executed(self):
            try:
                self.response = GetAllExperiencesInteractor(experience_repo=self.experience_repo,
                                                            permissions_validator=self.permissions_validator) \
                        .set_params(mine=self.mine, saved=self.saved, logged_person_id=self.logged_person_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_result_should_be_both_experiences(self):
            assert self.response == [self.experience_a, self.experience_b]
            return self

        def then_should_call_get_all_experience_with_logged_person_id_and_mine_params(self):
            self.experience_repo.get_all_experiences.assert_called_once_with(mine=self.mine, saved=self.saved,
                                                                             logged_person_id=self.logged_person_id)

        def then_validate_permissions_should_be_called_with_logged_person_id(self):
            self.permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id)
            return self

        def then_should_raise_no_logged_exception(self):
            assert type(self.error) is NoLoggedException
            return self


class TestCreateNewExperience(object):

    def test_creates_and_returns_experience(self):
        TestCreateNewExperience.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience() \
                .given_an_experience_repo_that_returns_that_experience_on_create() \
                .given_a_permissions_validator_that_returns_true() \
                .given_a_title() \
                .given_a_description() \
                .given_an_author_id() \
                .given_an_experience_validator_that_accepts_them() \
                .when_execute_interactor() \
                .then_result_should_be_the_experience() \
                .then_should_validate_permissions() \
                .then_repo_create_method_should_be_called_with_params() \
                .then_params_should_be_validated()

    def test_invalid_experience_returns_error_and_doesnt_create_it(self):
        TestCreateNewExperience.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience() \
                .given_an_experience_repo() \
                .given_a_title() \
                .given_a_description() \
                .given_an_author_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience_validator_that_raises_invalid_entity_exception() \
                .when_execute_interactor() \
                .then_should_raise_invalid_entity_exception() \
                .then_should_validate_permissions() \
                .then_params_should_be_validated() \
                .then_repo_create_method_should_not_be_called()

    def test_no_permissions_raises_exception(self):
        TestCreateNewExperience.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience() \
                .given_an_experience_repo() \
                .given_a_title() \
                .given_a_description() \
                .given_an_author_id() \
                .given_a_permissions_validator_that_raises_no_permission_exception() \
                .given_an_experience_validator_that_raises_invalid_entity_exception() \
                .when_execute_interactor() \
                .then_should_raise_no_permissions_exception() \
                .then_should_validate_permissions() \
                .then_repo_create_method_should_not_be_called()

    class ScenarioMaker(object):

        def __init__(self):
            self.author_id = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '5'
            return self

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

        def given_a_permissions_validator_that_returns_true(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.return_value = True
            return self

        def given_a_permissions_validator_that_raises_no_permission_exception(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.side_effect = NoPermissionException()
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
                self.response = CreateNewExperienceInteractor(self.experience_repo,
                                                              self.experience_validator, self.permissions_validator) \
                    .set_params(title=self.title, description=self.description,
                                logged_person_id=self.logged_person_id).execute()
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
            experience_params = Experience(title=self.title, description=self.description,
                                           author_id=self.logged_person_id)
            self.experience_repo.create_experience.assert_called_once_with(experience_params)
            return self

        def then_repo_create_method_should_not_be_called(self):
            self.experience_repo.create_experience.assert_not_called()
            return self

        def then_params_should_be_validated(self):
            experience_params = Experience(title=self.title, description=self.description,
                                           author_id=self.logged_person_id)
            self.experience_validator.validate_experience.assert_called_once_with(experience_params)
            return self

        def then_should_validate_permissions(self):
            self.permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id, wants_to_create_content=True)
            return self

        def then_should_raise_no_permissions_exception(self):
            assert type(self.error) is NoPermissionException
            return self


class TestModifyExperience(object):

    def test_gets_modifies_not_none_params_and_returns_experience(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_experience() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_another_experience_updated_with_that_params() \
                .given_an_experience_repo_that_returns_both_experiences_on_get_and_update() \
                .given_an_experience_validator_that_accepts() \
                .when_interactor_is_executed() \
                .then_result_should_be_second_experience() \
                .then_should_validate_permissions() \
                .then_get_experience_should_be_called_with_id_and_logged_person_id() \
                .then_experience_validation_should_be_called_with_updated_experience() \
                .then_update_experience_should_be_called_with_updated_experience()

    def test_invalid_experience_returns_error_and_doesnt_update_it(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience() \
                .given_another_experience_updated_with_that_params() \
                .given_an_experience_repo_that_returns_that_experience_on_get() \
                .given_an_experience_validator_that_raises_invalid_entity_exception() \
                .when_interactor_is_executed() \
                .then_should_raise_invalid_entity_exception() \
                .then_should_validate_permissions() \
                .then_get_experience_should_be_called_with_id_and_logged_person_id() \
                .then_experience_validation_should_be_called_with_updated_experience() \
                .then_update_experience_should_be_not_called()

    def test_unexistent_experience_returns_entity_does_not_exist_error(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience_repo_that_raises_entity_does_not_exist() \
                .given_an_experience_validator() \
                .when_interactor_is_executed() \
                .then_should_raise_entity_does_not_exists() \
                .then_should_validate_permissions() \
                .then_get_experience_should_be_called_with_id_and_logged_person_id() \
                .then_update_experience_should_be_not_called()

    def test_no_permissions_raises_expcetion(self):
        TestModifyExperience.ScenarioMaker() \
                .given_an_id() \
                .given_a_description() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_raises_no_permissions_exception() \
                .given_an_experience_repo_that_raises_entity_does_not_exist() \
                .given_an_experience_validator() \
                .when_interactor_is_executed() \
                .then_should_raise_no_permissions_exception() \
                .then_should_validate_permissions() \
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

        def given_a_permissions_validator_that_returns_true(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.return_value = True
            return self

        def given_a_permissions_validator_that_raises_no_permissions_exception(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.side_effect = NoPermissionException()
            return self

        def given_another_experience_updated_with_that_params(self):
            self.updated_experience = Experience(id=self.experience.id, title=self.experience.title,
                                                 description=self.description, author_id=self.experience.author_id,
                                                 author_username=self.experience.author_username)
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
                self.result = ModifyExperienceInteractor(self.experience_repo, self.experience_validator,
                                                         self.permissions_validator) \
                    .set_params(id=self.id, title=None, description=self.description,
                                logged_person_id=self.logged_person_id).execute()
            except Exception as e:
                print(e)
                self.error = e
            return self

        def then_result_should_be_second_experience(self):
            assert self.result == self.updated_experience
            return self

        def then_get_experience_should_be_called_with_id_and_logged_person_id(self):
            self.experience_repo.get_experience \
                    .assert_called_once_with(id=self.id, logged_person_id=self.logged_person_id)
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

        def then_should_validate_permissions(self):
            self.permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id,
                                             has_permissions_to_modify_experience=self.id)
            return self

        def then_should_raise_no_permissions_exception(self):
            assert type(self.error) is NoPermissionException
            return self


class TestUploadExperiencePictureInteractor(object):

    def test_validates_permissions_and_attach_picture_to_experience(self):
        TestUploadExperiencePictureInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience() \
                .given_an_experience_repo_that_returns_that_experience_on_attach() \
                .given_an_experience_id() \
                .given_a_picture() \
                .when_interactor_is_executed() \
                .then_should_validate_permissions() \
                .then_should_call_repo_attach_picture_to_experience() \
                .then_should_return_experience()

    def test_invalid_permissions_doesnt_attach_picture(self):
        TestUploadExperiencePictureInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_raises_no_permissions_exception() \
                .given_an_experience_repo() \
                .given_an_experience_id() \
                .given_a_picture() \
                .when_interactor_is_executed() \
                .then_should_validate_permissions() \
                .then_should_not_call_repo_attach_picture_to_experience() \
                .then_should_raise_no_permissions_exception()

    class ScenarioMaker(object):

        def given_a_logged_person_id(self):
            self.logged_person_id = '9'
            return self

        def given_a_permissions_validator_that_returns_true(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.return_value = True
            return self

        def given_a_permissions_validator_that_raises_no_permissions_exception(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.side_effect = NoPermissionException
            return self

        def given_an_experience(self):
            self.experience = Experience(id='2', title='T', description='s', author_id='4')
            return self

        def given_an_experience_repo_that_returns_that_experience_on_attach(self):
            self.experience_repo = Mock()
            self.experience_repo.attach_picture_to_experience.return_value = self.experience
            return self

        def given_an_experience_repo(self):
            self.experience_repo = Mock()
            return self

        def given_an_experience_id(self):
            self.experience_id = '5'
            return self

        def given_a_picture(self):
            self.picture = 'pic'
            return self

        def when_interactor_is_executed(self):
            try:
                interactor = UploadExperiencePictureInteractor(experience_repo=self.experience_repo,
                                                               permissions_validator=self.permissions_validator)
                self.result = interactor.set_params(experience_id=self.experience_id, picture=self.picture,
                                                    logged_person_id=self.logged_person_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_should_validate_permissions(self):
            self.permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id,
                                             has_permissions_to_modify_experience=self.experience_id)
            return self

        def then_should_call_repo_attach_picture_to_experience(self):
            self.experience_repo.attach_picture_to_experience.assert_called_once_with(experience_id=self.experience_id,
                                                                                      picture=self.picture)
            return self

        def then_should_return_experience(self):
            assert self.result == self.experience
            return self

        def then_should_not_call_repo_attach_picture_to_experience(self):
            self.experience_repo.attach_picture_to_experience.assert_not_called()
            return self

        def then_should_raise_no_permissions_exception(self):
            assert type(self.error) is NoPermissionException
            return self


class TestSaveUnsaveExperienceInteractor(object):

    def test_unauthorized_raises_no_logged_exception(self):
        TestSaveUnsaveExperienceInteractor.ScenarioMaker() \
                .given_a_permissions_validator_that_raises_no_permissions_exception() \
                .given_an_experience_repo_that_returns_true_on_save_and_others_experience() \
                .when_interactor_is_executed(action=SaveUnsaveExperienceInteractor.Action.SAVE) \
                .then_should_not_call_repo_save_experience() \
                .then_should_raise_no_logged_exception()

    def test_save_you_own_experience_raises_conflict_exception(self):
        TestSaveUnsaveExperienceInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience_id() \
                .given_an_experience_repo_that_returns_own_experience() \
                .when_interactor_is_executed(action=SaveUnsaveExperienceInteractor.Action.SAVE) \
                .then_should_validate_permissions() \
                .then_should_call_repo_get_experience_with_experience_id() \
                .then_should_not_call_repo_save_experience() \
                .then_should_raise_conflict_exception()

    def test_save_calls_repo_save_and_returns_true(self):
        TestSaveUnsaveExperienceInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience_id() \
                .given_an_experience_repo_that_returns_true_on_save_and_others_experience() \
                .when_interactor_is_executed(action=SaveUnsaveExperienceInteractor.Action.SAVE) \
                .then_should_validate_permissions() \
                .then_should_call_repo_get_experience_with_experience_id() \
                .then_should_call_repo_save_experience_with_person_id() \
                .then_should_return_true()

    def test_unsave_calls_repo_unsave_and_returns_true(self):
        TestSaveUnsaveExperienceInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_permissions_validator_that_returns_true() \
                .given_an_experience_id() \
                .given_an_experience_repo_that_returns_true_on_save_and_others_experience() \
                .when_interactor_is_executed(action=SaveUnsaveExperienceInteractor.Action.UNSAVE) \
                .then_should_validate_permissions() \
                .then_should_call_repo_get_experience_with_experience_id() \
                .then_should_call_repo_unsave_experience_with_person_id() \


    class ScenarioMaker(object):

        def __init__(self):
            self.experience_id = None
            self.logged_person_id = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '9'
            return self

        def given_a_permissions_validator_that_returns_true(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.return_value = True
            return self

        def given_a_permissions_validator_that_raises_no_permissions_exception(self):
            self.permissions_validator = Mock()
            self.permissions_validator.validate_permissions.side_effect = NoLoggedException
            return self

        def given_an_experience_repo_that_returns_true_on_save_and_others_experience(self):
            others_experience = Experience(id='4', title='t', description='d', author_id='3')
            self.experience_repo = Mock()
            self.experience_repo.save_experience.return_value = True
            self.experience_repo.get_experience.return_value = others_experience
            return self

        def given_an_experience_repo_that_returns_own_experience(self):
            others_experience = Experience(id='4', title='t', description='d', author_id=self.logged_person_id)
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = others_experience
            return self

        def given_an_experience_repo_that_returns_true_on_unsave(self):
            self.experience_repo = Mock()
            self.experience_repo.unsave_experience.return_value = True
            return self

        def given_an_experience_id(self):
            self.experience_id = '5'
            return self

        def when_interactor_is_executed(self, action):
            try:
                interactor = SaveUnsaveExperienceInteractor(experience_repo=self.experience_repo,
                                                            permissions_validator=self.permissions_validator)
                self.result = interactor.set_params(action=action, experience_id=self.experience_id,
                                                    logged_person_id=self.logged_person_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_should_validate_permissions(self):
            self.permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id)
            return self

        def then_should_call_repo_get_experience_with_experience_id(self):
            self.experience_repo.get_experience.assert_called_once_with(id=self.experience_id)
            return self

        def then_should_call_repo_save_experience_with_person_id(self):
            self.experience_repo.save_experience.assert_called_once_with(experience_id=self.experience_id,
                                                                         person_id=self.logged_person_id)
            return self

        def then_should_call_repo_unsave_experience_with_person_id(self):
            self.experience_repo.unsave_experience.assert_called_once_with(experience_id=self.experience_id,
                                                                           person_id=self.logged_person_id)
            return self

        def then_should_return_true(self):
            assert self.result is True
            return self

        def then_should_not_call_repo_save_experience(self):
            self.experience_repo.save_experience.assert_not_called()
            return self

        def then_should_raise_no_logged_exception(self):
            assert type(self.error) is NoLoggedException
            return self

        def then_should_raise_conflict_exception(self):
            assert type(self.error) is ConflictException
            assert self.error.source == 'experience'
            assert self.error.code == 'self_save'
            assert str(self.error) == 'You cannot save your own experiences'
            return self
