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
