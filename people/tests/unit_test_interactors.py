from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException, ConflictException, \
        UnauthorizedException
from people.entities import Person, AuthToken
from people.interactors import CreateGuestPersonAndReturnAuthTokenInteractor, AuthenticateInteractor, \
        RegisterUsernameAndEmailInteractor, ConfirmEmailInteractor


class TestCreateGuestPersonAndReturnAuthToken(object):

    def test_creates_guest_person_and_returns_auth_token(self):
        TestCreateGuestPersonAndReturnAuthToken._ScenarioMaker() \
                .given_a_client_secret_key() \
                .given_a_client_secret_key_validator_that_accepts_that_key() \
                .given_a_person_repo_that_returns_a_person() \
                .given_an_auth_token_repo_that_returns_a_token() \
                .when_execute_interactor() \
                .then_result_should_be_that_token() \
                .then_client_secret_key_should_be_validated() \
                .then_person_repo_create_guest_person_should_be_called() \
                .then_create_auth_token_should_be_called_with_returned_person_id()

    def test_invalid_client_secret_key_returns_invalid_entity_exception_and_doesnt_create_person(self):
        TestCreateGuestPersonAndReturnAuthToken._ScenarioMaker() \
                .given_a_client_secret_key() \
                .given_a_client_secret_key_validator_that_doesnt_accept_that_key() \
                .given_a_person_repo_that_returns_a_person() \
                .given_an_auth_token_repo_that_returns_a_token() \
                .when_execute_interactor() \
                .then_should_raise_invalid_entity_exception() \
                .then_client_secret_key_should_be_validated() \
                .then_person_repo_create_guest_person_should_not_be_called() \
                .then_create_auth_token_should_not_be_called()

    class _ScenarioMaker(object):

        def __init__(self):
            self.person = None
            self.auth_token = None
            self.person_repo = None
            self.auth_token_repo = None
            self.result = None
            self.client_secret_key = None
            self.client_secret_key_validator = None

        def given_a_client_secret_key(self):
            self.client_secret_key = "scrt"
            return self

        def given_a_client_secret_key_validator_that_accepts_that_key(self):
            self.client_secret_key_validator = Mock()
            self.client_secret_key_validator.validate.return_value = True
            return self

        def given_a_client_secret_key_validator_that_doesnt_accept_that_key(self):
            self.client_secret_key_validator = Mock()
            self.client_secret_key_validator.validate.side_effect = InvalidEntityException(
                    source='client_secret_key',
                    code='invalid',
                    message='Invalid client secret key')
            return self

        def given_a_person_repo_that_returns_a_person(self):
            self.person = Person(id='3')
            self.person_repo = Mock()
            self.person_repo.create_guest_person.return_value = self.person
            return self

        def given_an_auth_token_repo_that_returns_a_token(self):
            self.auth_token = AuthToken(person_id='3', access_token='A', refresh_token='R')
            self.auth_token_repo = Mock()
            self.auth_token_repo.create_auth_token.return_value = self.auth_token
            return self

        def when_execute_interactor(self):
            try:
                interactor = CreateGuestPersonAndReturnAuthTokenInteractor(
                        client_secret_key_validator=self.client_secret_key_validator,
                        person_repo=self.person_repo,
                        auth_token_repo=self.auth_token_repo)
                self.result = interactor.set_params(client_secret_key=self.client_secret_key).execute()
            except Exception as e:
                self.error = e
            return self

        def then_result_should_be_that_token(self):
            assert self.result == self.auth_token
            return self

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'client_secret_key'
            assert self.error.code == 'invalid'
            return self

        def then_client_secret_key_should_be_validated(self):
            self.client_secret_key_validator.validate.assert_called_once_with(client_secret_key=self.client_secret_key)
            return self

        def then_person_repo_create_guest_person_should_be_called(self):
            self.person_repo.create_guest_person.assert_called_once()
            return self

        def then_person_repo_create_guest_person_should_not_be_called(self):
            self.person_repo.create_guest_person.assert_not_called()
            return self

        def then_create_auth_token_should_be_called_with_returned_person_id(self):
            self.auth_token_repo.create_auth_token.assert_called_once_with(person_id=self.person.id)
            return self

        def then_create_auth_token_should_not_be_called(self):
            self.auth_token_repo.create_auth_token.assert_not_called()
            return self


class TestAuthenticateInteractor(object):

    def test_correct_access_token_returns_person_id(self):
        TestAuthenticateInteractor.ScenarioMaker() \
                .given_an_access_token() \
                .given_an_auth_token() \
                .given_an_auth_repo_that_returns_that_auth_token() \
                .when_authenticate_interactor_is_executed() \
                .then_should_call_repo_get_auth_token_with_access_token() \
                .then_should_return_auth_token_person_id()

    def test_wrong_access_token_returns_none(self):
        TestAuthenticateInteractor.ScenarioMaker() \
                .given_an_access_token() \
                .given_an_auth_repo_that_raises_entity_does_not_exist() \
                .when_authenticate_interactor_is_executed() \
                .then_should_return_none()

    class ScenarioMaker(object):

        def __init__(self):
            self.result = None
            self.repo = None
            self.access_token = None
            self.auth_token = None

        def given_an_access_token(self):
            self.access_token = 'A_T'
            return self

        def given_an_auth_token(self):
            self.auth_token = AuthToken(person_id='1', access_token='A', refresh_token='R')
            return self

        def given_an_auth_repo_that_returns_that_auth_token(self):
            self.repo = Mock()
            self.repo.get_auth_token.return_value = self.auth_token
            return self

        def given_an_auth_repo_that_raises_entity_does_not_exist(self):
            self.repo = Mock()
            self.repo.get_auth_token.side_effect = EntityDoesNotExistException
            return self

        def when_authenticate_interactor_is_executed(self):
            self.result = AuthenticateInteractor(self.repo).set_params(access_token=self.access_token).execute()
            return self

        def then_should_call_repo_get_auth_token_with_access_token(self):
            self.repo.get_auth_token.assert_called_once_with(access_token=self.access_token)
            return self

        def then_should_return_auth_token_person_id(self):
            assert self.result == self.auth_token.person_id
            return self

        def then_should_return_none(self):
            assert self.result is None
            return self


class TestRegisterUsernameAndEmailInteractor(object):

    def test_correct_username_and_email_updates_person_and_returns_it(self):
        TestRegisterUsernameAndEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_username_and_email() \
                .given_a_person_validator_that_accepts_them() \
                .given_a_first_person() \
                .given_a_second_person() \
                .given_a_person_repo() \
                .given_that_repo_returns_first_person_on_get() \
                .given_that_repo_returns_second_person_on_update() \
                .given_a_confirmation_token() \
                .given_confirmation_token_repo_that_returns_that_token() \
                .given_a_mailer_service() \
                .when_register_interactor_is_called() \
                .then_should_call_repo_get_with_logged_person_id() \
                .then_should_call_validate_with_new_username_and_email() \
                .then_should_call_repo_update_with_new_username_and_email() \
                .then_should_delete_previous_person_confirmation_tokens() \
                .then_should_create_confirmation_token() \
                .then_should_send_email_with_confirmation_token() \
                .then_result_should_be_second_person()

    def test_wrong_attributes_raises_invalid_entity_exception(self):
        TestRegisterUsernameAndEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_username_and_email() \
                .given_a_person_validator_that_raises_invalid_entity_exception() \
                .given_a_first_person() \
                .given_a_person_repo() \
                .given_that_repo_returns_first_person_on_get() \
                .given_confirmation_token_repo() \
                .given_a_mailer_service() \
                .when_register_interactor_is_called() \
                .then_should_call_repo_get_with_logged_person_id() \
                .then_should_call_validate_with_new_username_and_email() \
                .then_should_not_call_repo_update() \
                .then_should_not_delete_previous_person_confirmation_tokens() \
                .then_should_not_create_confirmation_token() \
                .then_should_not_send_email_with_confirmation_token() \
                .then_should_raise_invalid_entity_exception()

    def test_already_confirmed_email_doesnt_let_update_and_raises_conflict_exception(self):
        TestRegisterUsernameAndEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_person_with_confirmed_email() \
                .given_a_person_repo() \
                .given_that_repo_returns_first_person_on_get() \
                .given_confirmation_token_repo() \
                .given_a_mailer_service() \
                .when_register_interactor_is_called() \
                .then_should_call_repo_get_with_logged_person_id() \
                .then_should_not_call_repo_update() \
                .then_should_not_delete_previous_person_confirmation_tokens() \
                .then_should_not_create_confirmation_token() \
                .then_should_not_send_email_with_confirmation_token() \
                .then_should_raise_conflict_exception()

    def test_no_logged_person_id_raises_unauthorized(self):
        TestRegisterUsernameAndEmailInteractor.ScenarioMaker() \
                .given_a_person_repo() \
                .given_confirmation_token_repo() \
                .given_a_mailer_service() \
                .when_register_interactor_is_called() \
                .then_should_raise_unauthorized_exception() \
                .then_should_not_call_repo_update() \
                .then_should_not_delete_previous_person_confirmation_tokens() \
                .then_should_not_create_confirmation_token() \
                .then_should_not_send_email_with_confirmation_token() \


    class ScenarioMaker(object):

        def __init__(self):
            self.logged_person_id = None
            self.username = None
            self.email = None
            self.person_validator = None
            self.person = None
            self.second_person = None
            self.person_repo = None
            self.confirmation_token = None
            self.confirmation_token_repo = None
            self.mailer_service = None
            self.result = None
            self.error = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '5'
            return self

        def given_a_username_and_email(self):
            self.username = 'usr'
            self.email = 'e@m'
            return self

        def given_a_person_validator_that_accepts_them(self):
            self.person_validator = Mock()
            self.person_validator.validate.return_value = True
            return self

        def given_a_person_validator_that_raises_invalid_entity_exception(self):
            self.person_validator = Mock()
            self.person_validator.validate.side_effect = InvalidEntityException(source='username', code='already_used',
                                                                                message='Username already used')
            return self

        def given_a_first_person(self):
            self.person = Person(id='8', is_registered=True, username='u', email='e')
            return self

        def given_a_second_person(self):
            self.second_person = Person(id='9', is_registered=True, username='o', email='i')
            return self

        def given_a_person_with_confirmed_email(self):
            self.person = Person(id='8', is_registered=True, username='u', email='e', is_email_confirmed=True)
            return self

        def given_a_person_repo(self):
            self.person_repo = Mock()
            return self

        def given_that_repo_returns_first_person_on_get(self):
            self.person_repo.get_person.return_value = self.person
            return self

        def given_that_repo_returns_second_person_on_update(self):
            self.person_repo.update_person.return_value = self.second_person
            return self

        def given_a_confirmation_token(self):
            self.confirmation_token = 'K_T'
            return self

        def given_confirmation_token_repo_that_returns_that_token(self):
            self.given_confirmation_token_repo()
            self.confirmation_token_repo.create_confirmation_token.return_value = self.confirmation_token
            return self

        def given_confirmation_token_repo(self):
            self.confirmation_token_repo = Mock()
            return self

        def given_a_mailer_service(self):
            self.mailer_service = Mock()
            return self

        def when_register_interactor_is_called(self):
            try:
                interactor = RegisterUsernameAndEmailInteractor(person_validator=self.person_validator,
                                                                person_repo=self.person_repo,
                                                                confirmation_token_repo=self.confirmation_token_repo,
                                                                mailer_service=self.mailer_service)
                self.result = interactor.set_params(self.logged_person_id, self.username, self.email).execute()
            except Exception as e:
                print('ERROR')
                print(e)
                self.error = e
            return self

        def then_should_call_repo_get_with_logged_person_id(self):
            self.person_repo.get_person.assert_called_once_with(id=self.logged_person_id)
            return self

        def then_should_call_validate_with_new_username_and_email(self):
            self.person_validator.validate.assert_called_once_with(Person(id=self.person.id, is_registered=True,
                                                                          username=self.username, email=self.email,
                                                                          is_email_confirmed=False))
            return self

        def then_should_call_repo_update_with_new_username_and_email(self):
            self.person_repo.update_person.assert_called_once_with(Person(id=self.person.id, is_registered=True,
                                                                          username=self.username, email=self.email,
                                                                          is_email_confirmed=False))
            return self

        def then_should_delete_previous_person_confirmation_tokens(self):
            self.confirmation_token_repo.delete_confirmation_tokens \
                    .assert_called_once_with(person_id=self.second_person.id)
            return self

        def then_should_create_confirmation_token(self):
            self.confirmation_token_repo.create_confirmation_token \
                    .assert_called_once_with(person_id=self.second_person.id)
            return self

        def then_should_send_email_with_confirmation_token(self):
            self.mailer_service.send_ask_confirmation_mail.assert_called_once_with(
                    confirmation_token=self.confirmation_token,
                    username=self.second_person.username,
                    email=self.second_person.email)
            return self

        def then_result_should_be_second_person(self):
            assert self.result == self.second_person
            return self

        def then_should_not_call_repo_update(self):
            self.person_repo.update_person.assert_not_called()
            return self

        def then_should_not_delete_previous_person_confirmation_tokens(self):
            self.confirmation_token_repo.delete_confirmation_tokens.assert_not_called()
            return self

        def then_should_not_create_confirmation_token(self):
            self.confirmation_token_repo.create_confirmation_token.assert_not_called()
            return self

        def then_should_not_send_email_with_confirmation_token(self):
            self.mailer_service.send_ask_confirmation_mail.assert_not_called()
            return self

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'username'
            assert self.error.code == 'already_used'
            assert str(self.error) == 'Username already used'
            return self

        def then_should_raise_conflict_exception(self):
            assert type(self.error) is ConflictException
            assert self.error.source == 'person'
            assert self.error.code == 'already_registered'
            assert str(self.error) == 'Person already registered'
            return self

        def then_should_raise_unauthorized_exception(self):
            assert type(self.error) is UnauthorizedException
            return self


class TestConfirmEmailInteractor(object):

    def test_confirm_email_returns_person_confirmed(self):
        TestConfirmEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_confirmation_token() \
                .given_a_confirmation_token_repo_that_returns_that_confirmation_token() \
                .given_an_updated_person() \
                .given_a_person() \
                .given_a_person_repo_that_returns_those_persons_on_get_and_update() \
                .when_confirm_email_interactor_is_executed() \
                .then_should_call_confirmation_token_repo_get_person_id_with_confirmation_token() \
                .then_should_delete_all_confirmation_tokens_for_that_person() \
                .then_should_call_person_repo_get() \
                .then_should_call_person_repo_update_with_is_email_confirmed_true() \
                .then_should_return_person_confirmed()

    def test_unauthenticated_raises_unauthorized(self):
        TestConfirmEmailInteractor.ScenarioMaker() \
                .when_confirm_email_interactor_is_executed() \
                .then_should_raise_unauthorized() \
                .then_should_not_delete_all_confirmation_tokens_for_that_person() \
                .then_should_not_call_person_repo_update()

    def test_no_confirmation_token_raises_unauthorized(self):
        TestConfirmEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_confirmation_token_repo_that_raises_entity_does_not_exist() \
                .when_confirm_email_interactor_is_executed() \
                .then_should_raise_invalid_params_for_wrong_confirmation_token() \
                .then_should_not_delete_all_confirmation_tokens_for_that_person() \
                .then_should_not_call_person_repo_update()

    def test_not_coincident_person_id_raises_unauthorized(self):
        TestConfirmEmailInteractor.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_confirmation_token_repo_that_returns_another_person_id() \
                .when_confirm_email_interactor_is_executed() \
                .then_should_raise_invalid_params_for_wrong_confirmation_token() \
                .then_should_not_delete_all_confirmation_tokens_for_that_person() \
                .then_should_not_call_person_repo_update()

    class ScenarioMaker(object):

        def __init__(self):
            self.result = None
            self.error = None
            self.updated_person = None
            self.person = None
            self.logged_person_id = None
            self.confirmation_token = None
            self.confirmation_token_repo = Mock()
            self.person_repo = Mock()

        def given_a_logged_person_id(self):
            self.logged_person_id = '2'
            return self

        def given_a_confirmation_token(self):
            self.confirmation_token = 'ABC'
            return self

        def given_a_confirmation_token_repo_that_returns_that_confirmation_token(self):
            self.confirmation_token_repo.get_person_id.return_value = self.logged_person_id
            return self

        def given_a_confirmation_token_repo_that_returns_another_person_id(self):
            self.confirmation_token_repo.get_person_id.return_value = '99'
            return self

        def given_a_confirmation_token_repo_that_raises_entity_does_not_exist(self):
            self.confirmation_token_repo.get_person_id.side_effect = EntityDoesNotExistException()
            return self

        def given_a_person(self):
            self.person = Person(id='4', is_registered=True, username='usr', email='e@m.c', is_email_confirmed=False)
            return self

        def given_an_updated_person(self):
            self.updated_person = Person(id='4', is_registered=True, username='usr',
                                         email='e@m.c', is_email_confirmed=True)
            return self

        def given_a_person_repo_that_returns_those_persons_on_get_and_update(self):
            self.person_repo.update_person.return_value = self.updated_person
            self.person_repo.get_person.return_value = self.person
            return self

        def when_confirm_email_interactor_is_executed(self):
            try:
                interactor = ConfirmEmailInteractor(confirmation_token_repo=self.confirmation_token_repo,
                                                    person_repo=self.person_repo)
                self.result = interactor.set_params(logged_person_id=self.logged_person_id,
                                                    confirmation_token=self.confirmation_token).execute()
            except Exception as e:
                print(e)
                self.error = e
            return self

        def then_should_call_confirmation_token_repo_get_person_id_with_confirmation_token(self):
            self.confirmation_token_repo.get_person_id \
                    .assert_called_once_with(confirmation_token=self.confirmation_token)
            return self

        def then_should_delete_all_confirmation_tokens_for_that_person(self):
            self.confirmation_token_repo.delete_confirmation_tokens \
                    .assert_called_once_with(person_id=self.logged_person_id)
            return self

        def then_should_call_person_repo_get(self):
            self.person_repo.get_person.assert_called_once_with(id=self.logged_person_id)
            return self

        def then_should_call_person_repo_update_with_is_email_confirmed_true(self):
            update_person = Person(id=self.person.id, is_registered=self.person.is_registered,
                                   username=self.person.username, email=self.person.email, is_email_confirmed=True)
            self.person_repo.update_person.assert_called_once_with(update_person)
            return self

        def then_should_return_person_confirmed(self):
            assert self.result == self.updated_person
            return self

        def then_should_raise_unauthorized(self):
            assert type(self.error) is UnauthorizedException
            return self

        def then_should_not_delete_all_confirmation_tokens_for_that_person(self):
            self.confirmation_token_repo.delete_confirmation_tokens.assert_not_called()
            return self

        def then_should_not_call_person_repo_update(self):
            self.person_repo.update_person.assert_not_called()
            return self

        def then_should_raise_invalid_params_for_wrong_confirmation_token(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 'confirmation_token'
            assert self.error.code == 'invalid'
            assert str(self.error) == 'Invalid confirmation token'
            return self
