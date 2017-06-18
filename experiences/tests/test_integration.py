import json

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
                               'id': exp_a.id,
                               'title': 'Exp a',
                               'description': 'some description',
                               'picture': None
                           },
                           {
                               'id': exp_b.id,
                               'title': 'Exp b',
                               'description': 'other description',
                               'picture': None
                           },
                       ]


class ExperienceDetailTestCase(TestCase):

    def test_experience_detail_returns_experience(self):
        exp_c = ORMExperience.objects.create(title='Exp c', description='stuffs')

        client = Client()
        response = client.get(reverse('experience-detail', args=[exp_c.id]))

        assert response.status_code == 200
        body = json.loads(response.content)
        assert body == {
                           'id': exp_c.id,
                           'title': 'Exp c',
                           'description': 'stuffs',
                           'picture': None
                       }
