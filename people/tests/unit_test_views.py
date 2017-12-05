from mock import Mock

from people.entities import AuthToken
from people.views import PeopleView
from people.serializers import AuthTokenSerializer


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
