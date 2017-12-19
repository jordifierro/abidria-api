import json
import urllib.parse

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from experiences.models import ORMExperience
from people.models import ORMPerson, ORMAuthToken


class ExperiencesTestCase(TestCase):

    def test_mine_experiences_returns_my_experiences(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        exp_a = ORMExperience.objects.create(title='Exp a', description='some description', author=orm_person)
        exp_b = ORMExperience.objects.create(title='Exp b', description='other description', author=orm_person)

        client = Client()
        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.get("{}?mine=true".format(reverse('experiences')), **auth_headers)

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                           {
                               'id': str(exp_b.id),
                               'title': 'Exp b',
                               'description': 'other description',
                               'picture': None,
                               'author_id': orm_person.id,
                               'author_username': orm_person.username
                           },
                           {
                               'id': str(exp_a.id),
                               'title': 'Exp a',
                               'description': 'some description',
                               'picture': None,
                               'author_id': orm_person.id,
                               'author_username': orm_person.username
                           },
                       ]

    def test_not_mine_experiences_returns_others_experiences(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_person_b = ORMPerson.objects.create(username='nme')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person_b)
        exp_a = ORMExperience.objects.create(title='Exp a', description='some description', author=orm_person)
        exp_b = ORMExperience.objects.create(title='Exp b', description='other description', author=orm_person)

        client = Client()
        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.get(reverse('experiences'), **auth_headers)

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                           {
                               'id': str(exp_a.id),
                               'title': 'Exp a',
                               'description': 'some description',
                               'picture': None,
                               'author_id': orm_person.id,
                               'author_username': orm_person.username
                           },
                           {
                               'id': str(exp_b.id),
                               'title': 'Exp b',
                               'description': 'other description',
                               'picture': None,
                               'author_id': orm_person.id,
                               'author_username': orm_person.username
                           },
                       ]


class CreateExperienceTestCase(TestCase):

    def test_create_experience_creates_and_returns_experience(self):
        orm_person = ORMPerson.objects.create(username='usr.nm', is_email_confirmed=True)
        orm_auth_token = ORMAuthToken.objects.create(person_id=orm_person.id)
        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        client = Client()
        response = client.post(reverse('experiences'),
                               {'title': 'Experience title', 'description': 'Some description'},
                               **auth_headers)

        body = json.loads(response.content)
        created_experience = ORMExperience.objects.get(id=body['id'], title='Experience title',
                                                       description='Some description')
        assert created_experience is not None
        assert body == {
                           'id': str(created_experience.id),
                           'title': 'Experience title',
                           'description': 'Some description',
                           'picture': None,
                           'author_id': orm_person.id,
                           'author_username': orm_person.username
                       }

    def test_wrong_attributes_doesnt_create_and_returns_error(self):
        orm_person = ORMPerson.objects.create(is_email_confirmed=True)
        orm_auth_token = ORMAuthToken.objects.create(person_id=orm_person.id)
        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        client = Client()
        response = client.post(reverse('experiences'), {'title': '', 'description': 'Some description'}, **auth_headers)

        assert not ORMExperience.objects.filter(title='', description='Some description').exists()
        body = json.loads(response.content)
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'wrong_size',
                                        'message': 'Title must be between 1 and 30 chars'
                                    }
                       }


class ModifyExperienceTestCase(TestCase):

    def test_modifies_and_returns_experience(self):
        orm_person = ORMPerson.objects.create(username='usr.nm')
        orm_auth_token = ORMAuthToken.objects.create(person_id=orm_person.id)
        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        orm_experience = ORMExperience.objects.create(title='T', description='', author=orm_person)

        client = Client()
        response = client.patch(reverse('experience', args=[orm_experience.id]),
                                urllib.parse.urlencode({"description": "New description"}),
                                **auth_headers,
                                content_type='application/x-www-form-urlencoded')

        body = json.loads(response.content)
        updated_experience = ORMExperience.objects.get(id=orm_experience.id, title='T', description='New description')
        assert updated_experience is not None
        assert body == {
                           'id': str(orm_experience.id),
                           'title': 'T',
                           'description': 'New description',
                           'picture': None,
                           'author_id': orm_person.id,
                           'author_username': orm_person.username
                       }

    def test_wrong_attributes_doesnt_update_and_returns_error(self):
        orm_person = ORMPerson.objects.create()
        orm_auth_token = ORMAuthToken.objects.create(person_id=orm_person.id)
        orm_experience = ORMExperience.objects.create(title='T', description='', author=orm_person)

        auth_headers = {'HTTP_AUTHORIZATION': 'Token {}'.format(orm_auth_token.access_token), }
        client = Client()
        response = client.patch(reverse('experience', args=[orm_experience.id]),
                                urllib.parse.urlencode({"title": "", "description": "Some description"}),
                                content_type='application/x-www-form-urlencoded', **auth_headers)

        assert not ORMExperience.objects.filter(title='', description='Some description').exists()
        body = json.loads(response.content)
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'wrong_size',
                                        'message': 'Title must be between 1 and 30 chars'
                                    }
                       }
