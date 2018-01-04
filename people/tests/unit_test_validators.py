from mock import Mock

from abidria.exceptions import InvalidEntityException, NoLoggedException, NoPermissionException, \
        EntityDoesNotExistException
from people.validators import ClientSecretKeyValidator, PersonValidator, PersonPermissionsValidator
from people.entities import Person


class TestClientSecretKeyValidator:

    def test_valid_key(self):
        TestClientSecretKeyValidator._ScenarioMaker() \
                .given_a_client_secret_key_validator_with_valid_key('A') \
                .when_key_is_validated('A') \
                .then_response_should_be_true()

    def test_invalid_key(self):
        TestClientSecretKeyValidator._ScenarioMaker() \
                .given_a_client_secret_key_validator_with_valid_key('A') \
                .when_key_is_validated('B') \
                .then_should_raise_invalid_entity_execption()

    class _ScenarioMaker:

        def __init__(self):
            self.validator = None
            self.response = None
            self.error = None

        def given_a_client_secret_key_validator_with_valid_key(self, key):
            self.validator = ClientSecretKeyValidator(valid_client_secret_key=key)
            return self

        def when_key_is_validated(self, key):
            try:
                self.response = self.validator.validate(client_secret_key=key)
            except InvalidEntityException as e:
                self.error = e
            return self

        def then_response_should_be_true(self):
            assert self.response is True
            return self

        def then_should_raise_invalid_entity_execption(self):
            assert self.error.source == 'client_secret_key'
            assert self.error.code == 'invalid'
            assert str(self.error) == 'Invalid client secret key'
            return self


class TestPersonValidator:

    def test_valid_person(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_result_should_be_true()

    def test_short_username(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('aa') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_size_username()

    def test_long_username(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('a'*21) \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_size_username()

    def test_wrong_characters_or_order_usernames(self):
        wrong_usernames = ['.asdf', 'asdf.', '_asdf', 'asdf_', 'as..df', 'as_.df', 'as._df', 'as__df',
                           'asdf.', 'asdf_', 'asdfA', 'asdf#', 'asdf?', 'asdf/']
        for username in wrong_usernames:
            TestPersonValidator.ScenarioMaker() \
                .given_a_username(username) \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_username()

    def test_forbidden_username(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('ban') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_username()

    def test_username_that_contains_project_name(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('asdf_abidria_asdf') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_username()

    def test_mail_with_more_than_one_at(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_email()

    def test_empty_email(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_email()

    def test_mail_without_dots(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@m') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_email()

    def test_mail_without_ats(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('em.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_wrong_email()

    def test_forbidden_email(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_raises_entity_does_not_exists() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c', 'm.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_not_allowed_email()

    def test_already_used_username(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_returns_a_person_when_get_by_username() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c', 'm.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_username()

    def test_already_used_email(self):
        TestPersonValidator.ScenarioMaker() \
                .given_a_username('usr') \
                .given_an_email('e@m.c') \
                .given_a_person_with_that_params() \
                .given_a_repo_that_returns_a_person_when_get_by_email() \
                .given_a_person_validator_with_forbidden_usernames_and_email_domains(['ban'], ['i.c', 'm.c']) \
                .when_person_is_validated() \
                .then_should_raise_invalid_entity_exception_for_not_allowed_email()

    class ScenarioMaker:

        def __init__(self):
            self.username = None
            self.email = None
            self.person = None
            self.result = None
            self.error = None

        def given_a_username(self, username):
            self.username = username
            return self

        def given_an_email(self, email):
            self.email = email
            return self

        def given_a_person_with_that_params(self):
            self.person = Person(username=self.username, email=self.email)
            return self

        def given_a_person_validator_with_forbidden_usernames_and_email_domains(self, forbidden_usernames,
                                                                                forbidden_email_domains):
            self.validator = PersonValidator(project_name='abidria', forbidden_usernames=forbidden_usernames,
                                             forbidden_email_domains=forbidden_email_domains,
                                             person_repo=self.person_repo)
            return self

        def given_a_repo_that_raises_entity_does_not_exists(self):
            self.person_repo = Mock()
            self.person_repo.get_person.side_effect = EntityDoesNotExistException
            return self

        def given_a_repo_that_returns_a_person_when_get_by_username(self):
            def fake_get_person(username=None, email=None):
                if username is not None:
                    return self.person
                raise EntityDoesNotExistException()

            self.person_repo = Mock()
            self.person_repo.get_person = fake_get_person
            return self

        def given_a_repo_that_returns_a_person_when_get_by_email(self):
            def fake_get_person(username=None, email=None):
                if email is not None:
                    return self.person
                raise EntityDoesNotExistException()

            self.person_repo = Mock()
            self.person_repo.get_person = fake_get_person
            return self

        def when_person_is_validated(self):
            try:
                self.result = self.validator.validate(self.person)
            except Exception as e:
                self.error = e
            return self

        def then_result_should_be_true(self):
            assert self.result is True
            return self

        def then_should_raise_invalid_entity_exception_for_username(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'username'
            assert self.error.code == 'not_allowed'
            assert str(self.error) == 'Username not allowed'
            return self

        def then_should_raise_invalid_entity_exception_for_wrong_size_username(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'username'
            assert self.error.code == 'wrong_size'
            assert str(self.error) == 'Username length should be between 1 and 20 chars'
            return self

        def then_should_raise_invalid_entity_exception_for_not_allowed_email(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'email'
            assert self.error.code == 'not_allowed'
            assert str(self.error) == 'Email not allowed'
            return self

        def then_should_raise_invalid_entity_exception_for_wrong_email(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'email'
            assert self.error.code == 'wrong'
            assert str(self.error) == 'Email is wrong'
            return self


class TestPermissionsValidator:

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

    class ScenarioMaker:

        def __init__(self):
            self.logged_person_id = None
            self.person_repo = None
            self.wants_to_create_content = False

        def given_a_logged_person_id(self):
            self.logged_person_id = '4'
            return self

        def given_wants_to_create_contents(self):
            self.wants_to_create_content = True
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
            validator = PersonPermissionsValidator(person_repo=self.person_repo)
            try:
                self.result = validator.validate_permissions(self.logged_person_id,
                                                             wants_to_create_content=self.wants_to_create_content)
            except Exception as e:
                self.error = e
            return self

        def then_should_return_true(self):
            assert self.result is True
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
