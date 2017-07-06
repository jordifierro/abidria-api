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
