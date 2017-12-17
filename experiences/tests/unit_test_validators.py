from mock import Mock

from abidria.exceptions import InvalidEntityException, NoLoggedException, NoPermissionException
from experiences.validators import ExperienceValidator, PermissionsValidator
from experiences.entities import Experience
from people.entities import Person


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

    def test_no_logged_person(self):
        TestPermissionsValidator.ScenarioMaker() \
                .when_permission_is_validated() \
                .then_should_raise_no_logged_exception()

    def test_logged_with_no_experience_returns_true(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .when_permission_is_validated() \
                .then_should_return_true()

    def test_wants_to_create_content_but_doesnt_confirmed_email(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_wants_to_create_contents() \
                .given_a_person_repo_that_returns_a_person_without_email_confirmed() \
                .when_permission_is_validated() \
                .then_should_call_person_repo_get_with_logged_person_id() \
                .then_should_raise_no_permission_exception()

    def test_wants_to_create_content_and_has_email_confirmed_returns_true(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_wants_to_create_contents() \
                .given_a_person_repo_that_returns_a_person_with_email_confirmed() \
                .when_permission_is_validated() \
                .then_should_call_person_repo_get_with_logged_person_id() \
                .then_should_return_true()

    def test_no_experience_author_raises_no_permission_exception(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience_id() \
                .given_a_repo_that_returns_experience_with_other_author() \
                .when_permission_is_validated() \
                .then_should_call_repo_with_experience_id() \
                .then_should_raise_no_permission_exception()

    def test_is_experience_author_returns_true(self):
        TestPermissionsValidator.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience_id() \
                .given_a_repo_that_returns_experience_with_logged_person_as_author() \
                .when_permission_is_validated() \
                .then_should_call_repo_with_experience_id() \
                .then_should_return_true()

    class ScenarioMaker(object):

        def __init__(self):
            self.experience_repo = None
            self.logged_person_id = None
            self.experience_id = None
            self.person_repo = None
            self.wants_to_create_content = False

        def given_a_logged_person_id(self):
            self.logged_person_id = '4'
            return self

        def given_an_experience_id(self):
            self.experience_id = '9'
            return self

        def given_wants_to_create_contents(self):
            self.wants_to_create_content = True
            return self

        def given_a_repo_that_returns_experience_with_other_author(self):
            experience = Experience(id='1', title='t', description='d', author_id='999')
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = experience
            return self

        def given_a_repo_that_returns_experience_with_logged_person_as_author(self):
            experience = Experience(id='1', title='t', description='d', author_id=self.logged_person_id)
            self.experience_repo = Mock()
            self.experience_repo.get_experience.return_value = experience
            return self

        def given_a_person_repo_that_returns_a_person_without_email_confirmed(self):
            self.person_repo = Mock()
            person_without_confirmation = Person(id='2', is_registered=True, username='usr',
                                                 email='e@m.c', is_email_confirmed=False)
            self.person_repo.get_person.return_value = person_without_confirmation
            return self

        def given_a_person_repo_that_returns_a_person_with_email_confirmed(self):
            self.person_repo = Mock()
            person_with_confirmation = Person(id='2', is_registered=True, username='usr',
                                                 email='e@m.c', is_email_confirmed=True)
            self.person_repo.get_person.return_value = person_with_confirmation
            return self

        def when_permission_is_validated(self):
            validator = PermissionsValidator(experience_repo=self.experience_repo, person_repo=self.person_repo)
            try:
                self.result = validator \
                        .validate_permissions(self.logged_person_id,
                                              wants_to_create_content=self.wants_to_create_content,
                                              has_permissions_to_modify_experience=self.experience_id)
            except Exception as e:
                self.error = e
            return self

        def then_should_return_true(self):
            assert self.result is True
            return self

        def then_should_call_repo_with_experience_id(self):
            self.experience_repo.get_experience.assert_called_once_with(id=self.experience_id)
            return self

        def then_should_raise_no_logged_exception(self):
            assert type(self.error) is NoLoggedException
            return self

        def then_should_raise_no_permission_exception(self):
            assert type(self.error) is NoPermissionException
            return self

        def then_should_call_person_repo_get_with_logged_person_id(self):
            self.person_repo.get_person.assert_called_once_with(id=self.logged_person_id)
            return self
