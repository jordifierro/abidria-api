from mock import Mock

from people.entities import AuthToken, Person
from people.views import PeopleView, PersonView, EmailConfirmationView
from people.serializers import AuthTokenSerializer, PersonSerializer


class TestPeopleView(object):

    def test_post_returns_auth_token_serialized_and_201(self):
        TestPeopleView._ScenarioMaker() \
                .given_an_auth_token() \
                .given_an_interactor_that_returns_that_auth_token() \
                .given_a_client_secret_key() \
                .when_post_is_called_with_that_key() \
                .then_interactor_receives_that_key() \
                .then_response_status_is_201() \
                .then_response_body_is_auth_token_serialized()

    class _ScenarioMaker(object):

        def __init__(self):
            self.interactor_mock = Mock()
            self.interactor_mock.set_params.return_value = self.interactor_mock
            self.auth_token = None
            self.client_secret_key = None
            self.response = None

        def given_an_auth_token(self):
            self.auth_token = AuthToken(person_id='2', access_token='A', refresh_token='R')
            return self

        def given_a_client_secret_key(self):
            self.client_secret_key = 'scrt_ky'
            return self

        def given_an_interactor_that_returns_that_auth_token(self):
            self.interactor_mock.execute.return_value = self.auth_token
            return self

        def when_post_is_called_with_that_key(self):
            view = PeopleView(create_guest_person_and_return_auth_token_interactor=self.interactor_mock)
            self.body, self.status = view.post(client_secret_key=self.client_secret_key)
            return self

        def then_interactor_receives_that_key(self):
            self.interactor_mock.set_params.assert_called_once_with(client_secret_key=self.client_secret_key)
            return self

        def then_response_status_is_201(self):
            assert self.status == 201
            return self

        def then_response_body_is_auth_token_serialized(self):
            assert self.body == AuthTokenSerializer.serialize(self.auth_token)
            return self


class TestPersonView(object):

    def test_patch_returns_person_serialized_and_200(self):
        TestPersonView._ScenarioMaker() \
                .given_a_username() \
                .given_an_email() \
                .given_a_logged_person_id() \
                .given_a_person() \
                .given_an_interactor_that_returns_that_person() \
                .when_patch_is_called_with_that_params() \
                .then_interactor_receives_that_params() \
                .then_response_status_is_200() \
                .then_response_body_should_be_that_person_serialized()

    class _ScenarioMaker(object):

        def __init__(self):
            self.interactor_mock = Mock()
            self.interactor_mock.set_params.return_value = self.interactor_mock
            self.username = None
            self.email = None
            self.logged_person_id = None
            self.person = None
            self.response = None

        def given_a_username(self):
            self.username = 'usr.nm'
            return self

        def given_an_email(self):
            self.email = 'usr@em.c'
            return self

        def given_a_logged_person_id(self):
            self.logged_person_id = '4'
            return self

        def given_a_person(self):
            self.person = Person(id='8', is_registered=True, username='a', email='b', is_email_confirmed=False)
            return self

        def given_an_interactor_that_returns_that_person(self):
            self.interactor_mock.execute.return_value = self.person
            return self

        def when_patch_is_called_with_that_params(self):
            view = PersonView(register_username_and_email_interactor=self.interactor_mock)
            self.body, self.status = view.patch(logged_person_id=self.logged_person_id,
                                                username=self.username, email=self.email)
            return self

        def then_interactor_receives_that_params(self):
            self.interactor_mock.set_params.assert_called_once_with(logged_person_id=self.logged_person_id,
                                                                    username=self.username, email=self.email)
            return self

        def then_response_status_is_200(self):
            assert self.status == 200
            return self

        def then_response_body_should_be_that_person_serialized(self):
            assert self.body == PersonSerializer.serialize(self.person)
            return self


class TestEmailConfirmationView(object):

    def test_post_returns_204(self):
        TestEmailConfirmationView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_a_confirmation_token() \
                .when_post_is_called_with_that_params() \
                .then_interactor_receives_that_params() \
                .then_response_status_is_204() \
                .then_response_body_should_be_empty()

    class _ScenarioMaker(object):

        def __init__(self):
            self.interactor_mock = Mock()
            self.interactor_mock.set_params.return_value = self.interactor_mock
            self.logged_person_id = None
            self.confirmation_token = None
            self.response = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '4'
            return self

        def given_a_confirmation_token(self):
            self.confirmation_token = 'ABC'
            return self

        def when_post_is_called_with_that_params(self):
            view = EmailConfirmationView(confirm_email_interactor=self.interactor_mock)
            self.body, self.status = view.post(logged_person_id=self.logged_person_id,
                                               confirmation_token=self.confirmation_token)
            return self

        def then_interactor_receives_that_params(self):
            self.interactor_mock.set_params.assert_called_once_with(logged_person_id=self.logged_person_id,
                                                                    confirmation_token=self.confirmation_token)
            return self

        def then_response_status_is_204(self):
            assert self.status == 204
            return self

        def then_response_body_should_be_empty(self):
            assert self.body == ''
            return self
