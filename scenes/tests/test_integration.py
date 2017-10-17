import json
from decimal import Decimal

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from experiences.models import ORMExperience
from scenes.models import ORMScene


class ExperienceDetailTestCase(TestCase):

    def test_scenes_from_experience_returns_experience(self):
        exp_c = ORMExperience.objects.create(title='Exp c', description='stuffs')
        scene_d = ORMScene.objects.create(title='Scene d', description='D',
                                          latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience=exp_c)
        scene_e = ORMScene.objects.create(title='Scene e', description='E',
                                          latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience=exp_c)

        client = Client()
        response = client.get(reverse('scenes'), {'experience': str(exp_c.id)})

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


class CreateExperienceTestCase(TestCase):

    def test_create_experience_creates_and_returns_experience(self):
        experience = ORMExperience.objects.create(title='Exp')

        client = Client()
        response = client.post(reverse('scenes'), {'title': 'Scene title',
                                                   'description': 'Some description',
                                                   'latitude': 0.3,
                                                   'longitude': 1.2,
                                                   'experience_id': experience.id})

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
        experience = ORMExperience.objects.create(title='Exp')

        client = Client()
        response = client.post(reverse('scenes'), {'title': '',
                                                   'description': 'Some description',
                                                   'latitude': 0.3,
                                                   'longitude': 1.2,
                                                   'experience_id': experience.id})

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
