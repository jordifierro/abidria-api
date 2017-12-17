import json
from decimal import Decimal
import urllib.parse

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from experiences.models import ORMExperience
from scenes.models import ORMScene
from people.models import ORMPerson, ORMAuthToken


class ExperienceDetailTestCase(TestCase):

    def test_scenes_from_experience_returns_experience(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        exp_c = ORMExperience.objects.create(title='Exp c', description='stuffs', author=orm_person)
        scene_d = ORMScene.objects.create(title='Scene d', description='D',
                                          latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience=exp_c)
        scene_e = ORMScene.objects.create(title='Scene e', description='E',
                                          latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience=exp_c)

        client = Client()
        auth_headers = {'Authorization': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.get(reverse('scenes'), {'experience': str(exp_c.id)}, **auth_headers)

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == [
                            {
                                'id': str(scene_e.id),
                                'title': 'Scene e',
                                'description': 'E',
                                'picture': None,
                                'latitude': 5.6,
                                'longitude': -7.8,
                                'experience_id': str(exp_c.id),
                            },
                            {
                                'id': str(scene_d.id),
                                'title': 'Scene d',
                                'description': 'D',
                                'picture': None,
                                'latitude': 1.2,
                                'longitude': -3.4,
                                'experience_id': str(exp_c.id),
                            },
                       ]


class CreateSceneTestCase(TestCase):

    def test_create_scene_creates_and_returns_scene(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        experience = ORMExperience.objects.create(title='Exp', author=orm_person)

        client = Client()
        auth_headers = {'Authorization': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.post(reverse('scenes'), {'title': 'Scene title',
                                                   'description': 'Some description',
                                                   'latitude': 0.3,
                                                   'longitude': 1.2,
                                                   'experience_id': experience.id}, **auth_headers)

        body = json.loads(response.content)
        created_scene = ORMScene.objects.get(id=body['id'],
                                             title='Scene title',
                                             description='Some description',
                                             experience_id=experience.id)
        assert created_scene is not None
        assert body == {
                           'id': str(created_scene.id),
                           'title': 'Scene title',
                           'description': 'Some description',
                           'picture': None,
                           'latitude': 0.3,
                           'longitude': 1.2,
                           'experience_id': str(experience.id),
                       }

    def test_wrong_attributes_doesnt_create_and_returns_error(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        experience = ORMExperience.objects.create(title='Exp', author=orm_person)

        client = Client()
        auth_headers = {'Authorization': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.post(reverse('scenes'), {'title': '',
                                                   'description': 'Some description',
                                                   'latitude': 0.3,
                                                   'longitude': 1.2,
                                                   'experience_id': experience.id}, **auth_headers)

        assert not ORMScene.objects.filter(title='',
                                           description='Some description',
                                           latitude=0.3,
                                           longitude=1.2,
                                           experience_id=experience.id).exists()
        body = json.loads(response.content)
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'wrong_size',
                                        'message': 'Title must be between 1 and 30 chars'
                                    }
                       }


class ModifySceneTestCase(TestCase):

    def test_modifies_and_returns_scene(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        experience = ORMExperience.objects.create(title='Exp', author=orm_person)
        orm_scene = ORMScene.objects.create(title='T', description='',
                                            latitude=1, longitude=2, experience_id=experience.id)

        client = Client()
        auth_headers = {'Authorization': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.patch(reverse('scene', args=[orm_scene.id]),
                                urllib.parse.urlencode({"description": "New description",
                                                        "latitude": 0.3, "longitude": 1.2}),
                                content_type='application/x-www-form-urlencoded',
                                **auth_headers)

        body = json.loads(response.content)
        updated_scene = ORMScene.objects.get(id=orm_scene.id,
                                             title='T', description='New description',
                                             experience_id=experience.id)
        assert updated_scene is not None
        assert body == {
                           'id': str(orm_scene.id),
                           'title': 'T',
                           'description': 'New description',
                           'picture': None,
                           'latitude': 0.3,
                           'longitude': 1.2,
                           'experience_id': str(experience.id),
                       }

    def test_wrong_attributes_doesnt_update_and_returns_error(self):
        orm_person = ORMPerson.objects.create(username='usr')
        orm_auth_token = ORMAuthToken.objects.create(person=orm_person)
        experience = ORMExperience.objects.create(title='Exp', author=orm_person)
        orm_scene = ORMScene.objects.create(title='T', description='',
                                            latitude=1, longitude=2, experience_id=experience.id)

        client = Client()
        auth_headers = {'Authorization': 'Token {}'.format(orm_auth_token.access_token), }
        response = client.patch(reverse('scene', args=[orm_scene.id]),
                                urllib.parse.urlencode({"title": "",
                                                        "description": "Some description",
                                                        "latitude": 0.3,
                                                        "longitude": 1.2,
                                                        "experience_id": experience.id}),
                                content_type='application/x-www-form-urlencoded',
                                **auth_headers)

        assert not ORMScene.objects.filter(title='',
                                           description='Some description',
                                           latitude=0.3,
                                           longitude=1.2,
                                           experience_id=experience.id).exists()
        body = json.loads(response.content)
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'wrong_size',
                                        'message': 'Title must be between 1 and 30 chars'
                                    }
                       }
