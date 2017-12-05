from django.test import TestCase

from people.models import ORMPerson, ORMAuthToken
from people.repositories import PersonRepo, AuthTokenRepo


class PersonRepoTestCase(TestCase):

    def test_create_guest_person(self):
        PersonRepoTestCase._ScenarioMaker() \
                .when_create_guest_person() \
                .then_response_should_be_a_guest_person() \
                .then_that_person_should_be_saved_in_db()

    class _ScenarioMaker(object):

        def __init__(self):
            self.response = None

        def when_create_guest_person(self):
            self.result = PersonRepo().create_guest_person()
            return self

        def then_response_should_be_a_guest_person(self):
            assert self.result.id is not None
            assert not self.result.is_registered
            assert self.result.username is None
            assert self.result.email is None
            assert not self.result.is_email_confirmed
            return self

        def then_that_person_should_be_saved_in_db(self):
            assert ORMPerson.objects.filter(id=self.result.id).exists()


class AuthTokenRepoTestCase(TestCase):

    def test_create_auth_token(self):
        AuthTokenRepoTestCase._ScenarioMaker() \
                .given_a_person() \
                .when_create_auth_token_for_that_person() \
                .then_response_should_be_that_token() \
                .then_that_token_should_be_saved_in_db()

    class _ScenarioMaker(object):

        def __init__(self):
            self.person = None
            self.response = None

        def given_a_person(self):
            self.person = PersonRepo().create_guest_person()
            return self

        def when_create_auth_token_for_that_person(self):
            self.result = AuthTokenRepo().create_auth_token(person_id=self.person.id)
            return self

        def then_response_should_be_that_token(self):
            assert self.result.person_id == self.person.id
            assert type(self.result.access_token) is str
            assert type(self.result.refresh_token) is str
            return self

        def then_that_token_should_be_saved_in_db(self):
            assert ORMAuthToken.objects.filter(person_id=self.result.person_id, access_token=self.result.access_token,
                                               refresh_token=self.result.refresh_token).exists()
