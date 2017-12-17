from mock import Mock

from abidria.exceptions import InvalidEntityException, NoPermissionException
from experiences.validators import ExperienceValidator, ExperiencePermissionsValidator
from experiences.entities import Experience


class TestExperienceValidator(object):

    def test_valid_experience_returns_true(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience() \
                .when_experience_is_validated() \
                .then_response_should_be_true()

    def test_no_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title=None) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='empty_attribute',
                                             message='Title cannot be empty')

    def test_wrong_type_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title=1) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_type',
                                             message='Title must be string')

    def test_void_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title='') \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_size',
                                             message='Title must be between 1 and 30 chars')

    def test_large_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title='*'*31) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_size',
                                             message='Title must be between 1 and 30 chars')

    def test_wrong_type_description_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(description=1) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='description', code='wrong_type',
                                             message='Description must be string')

    def test_no_author_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(author_id=None) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='author', code='empty_attribute',
                                             message='Author cannot be empty')

    class _ScenarioMaker(object):

        def __init__(self):
            self._experience_repo = Mock()
            self._experience_repo.get_experience.return_value = True
            self._experience = None
            self._response = None
            self._error = None

        def given_an_experience(self, title='Valid Title', description=None, author_id='2'):
            self._experience = Experience(title=title, description=description, author_id=author_id)
            return self

        def when_experience_is_validated(self):
            validator = ExperienceValidator()
            try:
                self._response = validator.validate_experience(self._experience)
            except InvalidEntityException as e:
                self._error = e
            return self

        def then_response_should_be_true(self):
            assert self._response is True
            return self

        def then_error_should_be_raised(self, source=None, code=None, message=None):
            assert self._error.source == source
            assert self._error.code == code
            assert str(self._error) == message
            return self


class TestPermissionsValidator(object):

    def test_no_person_permissions(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_person_permission_validator_that_raises_no_permission_exception() \
                .when_permission_is_validated() \
                .then_should_call_person_permission_validator_with_logged_person_id() \
                .then_should_raise_no_permission_exception()

    def test_person_permission_but_different_person_id_raises_no_permission(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_person_permission_validator_that_returns_true() \
                .given_an_experience_id() \
                .given_an_experience_with_different_author_than_logged_person_id() \
                .given_an_experience_repo_that_returns_that_experience() \
                .when_permission_is_validated() \
                .then_should_call_person_permission_validator_with_logged_person_id() \
                .then_should_call_repo_get_experience_with_experience_id() \
                .then_should_raise_no_permission_exception()

    def test_person_permission_with_same_person_id(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_person_permission_validator_that_returns_true() \
                .given_an_experience_id() \
                .given_an_experience_with_same_author_than_logged_person_id() \
                .given_an_experience_repo_that_returns_that_experience() \
                .when_permission_is_validated() \
                .then_should_call_person_permission_validator_with_logged_person_id() \
                .then_should_call_repo_get_experience_with_experience_id() \
                .then_should_return_true()

    class ScenarioMaker(object):

        def __init__(self):
            self.experience_repo = None
            self.logged_person_id = None
            self.experience_id = None
            self.person_repo = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '4'
            return self

        def given_an_experience_id(self):
            self.experience_id = '9'
            return self

        def given_an_experience_with_same_author_than_logged_person_id(self):
            self.experience = Experience(id='1', title='t', description='d', author_id=self.logged_person_id)
            return self

        def given_an_experience_with_different_author_than_logged_person_id(self):
            self.experience = Experience(id='1', title='t', description='d', author_id='33')
            return self

        def given_a_person_permission_validator_that_raises_no_permission_exception(self):
            self.person_permissions_validator = Mock()
            self.person_permissions_validator.validate_permissions.side_effect = NoPermissionException()
            return self

        def given_a_person_permission_validator_that_returns_true(self):
            self.person_permissions_validator = Mock()
            self.person_permissions_validator.validate_permissions.return_value = True
            return self

        def given_an_experience_repo_that_returns_that_experience(self):
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = self.experience
            return self

        def when_permission_is_validated(self):
            validator = ExperiencePermissionsValidator(experience_repo=self.experience_repo,
                                                       person_permissions_validator=self.person_permissions_validator)
            try:
                self.result = validator.validate_permissions(self.logged_person_id,
                                                             has_permissions_to_modify_experience=self.experience_id)
            except Exception as e:
                self.error = e
            return self

        def then_should_return_true(self):
            assert self.result is True
            return self

        def then_should_call_repo_get_experience_with_experience_id(self):
            self.experience_repo.get_experience.assert_called_once_with(id=self.experience_id)
            return self

        def then_should_raise_no_permission_exception(self):
            assert type(self.error) is NoPermissionException
            return self

        def then_should_call_person_permission_validator_with_logged_person_id(self):
            self.person_permissions_validator.validate_permissions \
                    .assert_called_once_with(logged_person_id=self.logged_person_id)
            return self
