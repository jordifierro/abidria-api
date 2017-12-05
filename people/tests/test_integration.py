import json

from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from people.models import ORMAuthToken, ORMPerson


class CreatePersonTestCase(TestCase):

    def test_creates_guest_person_and_returns_auth_token(self):
        CreatePersonTestCase._ScenarioMaker() \
                .given_a_client_secret_key() \
                .when_people_post_is_called_with_that_client_secret_key() \
                .then_response_status_should_be_201() \
                .then_response_body_should_be_an_auth_token() \
                .then_a_person_has_that_auth_token()

    def test_wrong_client_secret_key_returns_error(self):
        CreatePersonTestCase._ScenarioMaker() \
                .given_a_client_secret_key() \
                .when_people_post_is_called_with_other_client_secret_key() \
                .then_response_status_should_be_422() \
                .then_response_body_should_be_an_error() \


    class _ScenarioMaker(object):

        def __init__(self):
            self.orm_person = None
            self.orm_auth_token = None
            self.response = None
            self.client_secret_key = None

        def given_a_client_secret_key(self):
            self.client_secret_key = "scrt"
            settings.CLIENT_SECRET_KEY = self.client_secret_key
            return self

        def when_people_post_is_called_with_that_client_secret_key(self):
            client = Client()
            self.response = client.post(reverse('people'), {'client_secret_key': self.client_secret_key})
            return self

        def when_people_post_is_called_with_other_client_secret_key(self):
            client = Client()
            self.response = client.post(reverse('people'), {'client_secret_key': 'wrong_key'})
            return self

        def then_response_status_should_be_201(self):
            assert self.response.status_code == 201
            return self

        def then_response_status_should_be_422(self):
            assert self.response.status_code == 422
            return self

        def then_response_body_should_be_an_auth_token(self):
            body = json.loads(self.response.content)
            assert body['access_token'] is not None
            assert body['refresh_token'] is not None
            return self

        def then_response_body_should_be_an_error(self):
            body = json.loads(self.response.content)
            assert body == {
                    'error': {
                        'source': 'client_secret_key',
                        'code': 'invalid',
                        'message': 'Invalid client secret key'
                        }
                    }
            return self

        def then_a_person_has_that_auth_token(self):
            body = json.loads(self.response.content)
            orm_auth_token = ORMAuthToken.objects.get(access_token=body['access_token'],
                                                      refresh_token=body['refresh_token'])
            orm_person = ORMPerson.objects.get(id=orm_auth_token.person_id)
            assert orm_person is not None
            return self
