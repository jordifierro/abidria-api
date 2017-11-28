import json
import urllib.parse

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from experiences.models import ORMExperience


class ExperiencesTestCase(TestCase):

    def test_experiences_returns_all_experiences(self):
        exp_a = ORMExperience.objects.create(title='Exp a', description='some description')
        exp_b = ORMExperience.objects.create(title='Exp b', description='other description')

        client = Client()
        response = client.get(reverse('experiences'))

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                           {
                               'id': str(exp_a.id),
                               'title': 'Exp a',
                               'description': 'some description',
                               'picture': None
                           },
                           {
                               'id': str(exp_b.id),
                               'title': 'Exp b',
                               'description': 'other description',
                               'picture': None
                           },
                       ]


class CreateExperienceTestCase(TestCase):

    def test_create_experience_creates_and_returns_experience(self):
        client = Client()
        response = client.post(reverse('experiences'), {'title': 'Experience title',
                                                        'description': 'Some description'})

        body = json.loads(response.content)
        created_experience = ORMExperience.objects.get(id=body['id'], title='Experience title',
                                                       description='Some description')
        assert created_experience is not None
        assert body == {
                           'id': str(created_experience.id),
                           'title': 'Experience title',
                           'description': 'Some description',
                           'picture': None,
                       }

    def test_wrong_attributes_doesnt_create_and_returns_error(self):
        client = Client()
        response = client.post(reverse('experiences'), {'title': '', 'description': 'Some description'})

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
        orm_experience = ORMExperience.objects.create(title='T', description='')

        client = Client()
        response = client.patch(reverse('experience', args=[orm_experience.id]),
                                urllib.parse.urlencode({"description": "New description"}),
                                content_type='application/x-www-form-urlencoded')

        body = json.loads(response.content)
        updated_experience = ORMExperience.objects.get(id=orm_experience.id, title='T', description='New description')
        assert updated_experience is not None
        assert body == {
                           'id': str(orm_experience.id),
                           'title': 'T',
                           'description': 'New description',
                           'picture': None,
                       }

    def test_wrong_attributes_doesnt_update_and_returns_error(self):
        orm_experience = ORMExperience.objects.create(title='T', description='')

        client = Client()
        response = client.patch(reverse('experience', args=[orm_experience.id]),
                                urllib.parse.urlencode({"title": "", "description": "Some description"}),
                                content_type='application/x-www-form-urlencoded')

        assert not ORMExperience.objects.filter(title='', description='Some description').exists()
        body = json.loads(response.content)
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'wrong_size',
                                        'message': 'Title must be between 1 and 30 chars'
                                    }
                       }
