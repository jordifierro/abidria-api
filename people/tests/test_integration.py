import json
import urllib.parse
import uuid

from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.template.loader import get_template

from people.models import ORMAuthToken, ORMPerson, ORMConfirmationToken


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


class ModifyPersonTestCase(TestCase):

    def test_modify_person_username_and_email(self):
        ModifyPersonTestCase._ScenarioMaker() \
                .given_a_guest_person_in_db_with_auth_token() \
                .given_a_confirmation_token_for_that_person() \
                .given_another_confirmation_token_for_that_person() \
                .given_a_username() \
                .given_an_email() \
                .when_that_person_call_patch_people_me_with_that_params() \
                .then_response_status_should_be_200() \
                .then_response_body_should_be_person_info() \
                .then_person_should_be_updated_and_marked_as_registered() \
                .then_old_confirmation_tokens_should_be_deleted() \
                .then_ask_confirmation_email_should_be_sent()

    def test_wrong_client_secret_key_returns_error(self):
        ModifyPersonTestCase._ScenarioMaker() \
                .given_a_registered_and_confirmed_person() \
                .given_a_username() \
                .given_an_email() \
                .when_that_person_call_patch_people_me_with_that_params() \
                .then_response_status_should_be_409() \
                .then_response_body_should_be_conflict_error() \
                .then_person_not_should_be_updated() \
                .then_ask_confirmation_email_should_not_be_sent()

    class _ScenarioMaker(object):

        def __init__(self):
            self.orm_person = None
            self.orm_confirmation_token = None
            self.orm_confirmation_token_2 = None
            self.username = None
            self.email = None
            self.response = None

        def given_a_guest_person_in_db_with_auth_token(self):
            self.orm_person = ORMPerson.objects.create()
            self.orm_auth_token = ORMAuthToken.objects.create(person_id=self.orm_person.id)
            return self

        def given_a_registered_and_confirmed_person(self):
            self.orm_person = ORMPerson.objects.create(username='u', email='e@m.c',
                                                       is_registered=True, is_email_confirmed=True)
            self.orm_auth_token = ORMAuthToken.objects.create(person_id=self.orm_person.id)
            return self

        def given_a_confirmation_token_for_that_person(self):
            self.orm_confirmation_token = ORMConfirmationToken.objects.create(person_id=self.orm_person.id)
            return self

        def given_another_confirmation_token_for_that_person(self):
            self.orm_confirmation_token_2 = ORMConfirmationToken.objects.create(person_id=self.orm_person.id)
            return self

        def given_a_username(self):
            self.username = 'usr.nm'
            return self

        def given_an_email(self):
            self.email = 'usr@m.c'
            return self

        def when_that_person_call_patch_people_me_with_that_params(self):
            client = Client()
            auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.orm_auth_token.access_token), }
            self.response = client.patch(reverse('person'),
                                         urllib.parse.urlencode({'username': self.username, 'email': self.email}),
                                         content_type='application/x-www-form-urlencoded',
                                         **auth_headers)
            return self

        def then_response_status_should_be_200(self):
            assert self.response.status_code == 200
            return self

        def then_response_body_should_be_person_info(self):
            body = json.loads(self.response.content)
            assert body['username'] == self.username
            assert body['email'] == self.email
            assert body['is_registered'] is True
            assert body['is_email_confirmed'] is False
            return self

        def then_person_should_be_updated_and_marked_as_registered(self):
            orm_updated_person = ORMPerson.objects.get(id=self.orm_person.id)
            assert orm_updated_person.username == self.username
            assert orm_updated_person.email == self.email
            assert orm_updated_person.is_registered is True
            assert orm_updated_person.is_email_confirmed is False
            return self

        def then_old_confirmation_tokens_should_be_deleted(self):
            assert not ORMConfirmationToken.objects.filter(token=self.orm_confirmation_token.token).exists()
            assert not ORMConfirmationToken.objects.filter(token=self.orm_confirmation_token_2.token).exists()
            return self

        def then_ask_confirmation_email_should_be_sent(self):
            assert mail.outbox[0].subject == 'Abidria account confirmation'
            confirmation_token = ORMConfirmationToken.objects.get(person_id=self.orm_person.id).token
            confirmation_reverse_url = self.response.wsgi_request.build_absolute_uri(reverse('email-confirmation'))
            confirmation_url = "{}?token={}".format(confirmation_reverse_url, confirmation_token)
            context_params = {'username': self.username, 'confirmation_url': confirmation_url}
            plain_text_message = get_template('ask_confirmation_email.txt').render(context_params)
            html_message = get_template('ask_confirmation_email.html').render(context_params)
            assert mail.outbox[0].body == plain_text_message
            assert mail.outbox[0].from_email == settings.EMAIL_HOST_USER
            assert mail.outbox[0].to == [self.email, ]
            assert mail.outbox[0].alternatives[0][0] == html_message
            return self

        def then_response_status_should_be_409(self):
            assert self.response.status_code == 409
            return self

        def then_response_body_should_be_conflict_error(self):
            body = json.loads(self.response.content)
            assert body == {
                    'error': {
                        'source': 'person',
                        'code': 'already_registered',
                        'message': 'Person already registered'
                        }
                    }
            return self

        def then_person_not_should_be_updated(self):
            orm_updated_person = ORMPerson.objects.get(id=self.orm_person.id)
            assert orm_updated_person.username != self.username
            assert orm_updated_person.email != self.email
            assert orm_updated_person.is_registered is True
            assert orm_updated_person.is_email_confirmed is True
            return self

        def then_ask_confirmation_email_should_not_be_sent(self):
            assert len(mail.outbox) == 0
            return self


class PostEmailConfirmationTestCase(TestCase):

    def test_post_email_confirmations_confirms_person_email(self):
        PostEmailConfirmationTestCase.ScenarioMaker() \
                .given_an_unconfirmed_registered_person() \
                .given_an_auth_token_for_that_person() \
                .given_a_confirmation_token_for_that_person() \
                .when_post_email_confirmation() \
                .then_response_should_be_204_empty_body() \
                .then_person_should_have_is_email_confirmed_true() \
                .then_confirmation_token_should_be_removed()

    def test_post_email_confirmation_with_invalid_token_returns_error(self):
        PostEmailConfirmationTestCase.ScenarioMaker() \
                .given_an_unconfirmed_registered_person() \
                .given_an_auth_token_for_that_person() \
                .given_a_fake_confirmation_token() \
                .when_post_email_confirmation() \
                .then_response_code_should_be_422() \
                .then_response_body_should_be_invalide_token_error() \
                .then_person_should_have_is_email_confirmed_false()

    class ScenarioMaker(object):

        def __init__(self):
            self.orm_person = None
            self.orm_auth_token = None
            self.orm_confirmation_token = None
            self.result = None

        def given_an_unconfirmed_registered_person(self):
            self.orm_person = ORMPerson.objects.create(is_registered=True, username='usr',
                                                       email='e@m.c', is_email_confirmed=False)
            return self

        def given_an_auth_token_for_that_person(self):
            self.orm_auth_token = ORMAuthToken.objects.create(person_id=self.orm_person.id)
            return self

        def given_a_confirmation_token_for_that_person(self):
            self.orm_confirmation_token = ORMConfirmationToken.objects.create(person_id=self.orm_person.id)
            self.confirmation_token = self.orm_confirmation_token.token
            return self

        def given_a_fake_confirmation_token(self):
            self.confirmation_token = uuid.uuid4()
            return self

        def when_post_email_confirmation(self):
            client = Client()
            auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.orm_auth_token.access_token), }
            self.response = client.post(reverse('email-confirmation'),
                                        urllib.parse.urlencode({'confirmation_token': self.confirmation_token}),
                                        content_type='application/x-www-form-urlencoded',
                                        **auth_headers)
            return self

        def then_response_should_be_204_empty_body(self):
            self.response.status_code == 204
            self.response.content == ''
            return self

        def then_person_should_have_is_email_confirmed_true(self):
            assert ORMPerson.objects.get(id=self.orm_person.id).is_email_confirmed is True
            return self

        def then_confirmation_token_should_be_removed(self):
            assert not ORMConfirmationToken.objects.filter(token=self.orm_confirmation_token.token).exists()
            return self

        def then_response_code_should_be_422(self):
            assert self.response.status_code == 422
            return self

        def then_response_body_should_be_invalide_token_error(self):
            body = json.loads(self.response.content)
            assert body == {
                    'error': {
                        'source': 'confirmation_token',
                        'code': 'invalid',
                        'message': 'Invalid confirmation token'
                        }
                    }
            return self

        def then_person_should_have_is_email_confirmed_false(self):
            assert ORMPerson.objects.get(id=self.orm_person.id).is_email_confirmed is False
            return self
