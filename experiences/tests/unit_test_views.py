import sys
from decimal import Decimal

from mock import Mock

from abidria.entities import Picture
from experiences.entities import Experience
from scenes.entities import Scene


class TestExperiencesView(object):

    def test_returns_experiences_serialized_and_200(self):
        picture_a = Picture(small='small.a', medium='medium.a', large='large.a')
        experience_a = Experience(id=1, title='A', description='some', picture=picture_a)
        picture_b = Picture(small='small.b', medium='medium.b', large='large.b')
        experience_b = Experience(id=2, title='B', description='other', picture=picture_b)

        factories_mock = Mock()
        factories_mock.GetAllExperiencesFactory.get().execute = Mock(return_value=[experience_a, experience_b])
        reset_imports_and_set_factories_module(factories_mock)
        from experiences.views import ExperiencesView

        body, status = ExperiencesView().get()

        assert status == 200
        assert body == [
                           {
                               'id': 1,
                               'title': 'A',
                               'description': 'some',
                               'picture': {'small': 'small.a',
                                           'medium': 'medium.a',
                                           'large': 'large.a'}
                           },
                           {
                               'id': 2,
                               'title': 'B',
                               'description': 'other',
                               'picture': {'small': 'small.b',
                                           'medium': 'medium.b',
                                           'large': 'large.b'}
                           },
                       ]
        sys.modules['experiences.factories'] = factories_mock


class TestExperienceDetailView(object):

    def test_returns_experience_and_scenes_serialized_and_200(self):
        picture_a = Picture(small='small.a', medium='medium.a', large='large.a')
        experience_a = Experience(id=1, title='A', description='some', picture=picture_a)

        picture_b = Picture(small='small.b', medium='medium.b', large='large.b')
        picture_c = Picture(small='small.c', medium='medium.c', large='large.c')
        scene_b = Scene(id=1, title='B', description='some', picture=picture_b,
                        latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id=1)
        scene_c = Scene(id=2, title='C', description='other', picture=picture_c,
                        latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=1)

        get_experience_mock = Mock()
        get_experience_mock.set_params = Mock(return_value=get_experience_mock)
        get_experience_mock.execute = Mock(return_value=(experience_a, [scene_b, scene_c]))

        factories_mock = Mock()
        factories_mock.GetExperienceFactory.get = Mock(return_value=get_experience_mock)
        reset_imports_and_set_factories_module(factories_mock)
        from experiences.views import ExperienceDetailView

        body, status = ExperienceDetailView().get(id='1')

        get_experience_mock.set_params.assert_called_once_with(id=1)
        assert status == 200
        assert body == {
                           'id': 1,
                           'title': 'A',
                           'description': 'some',
                           'picture': {
                               'small': 'small.a',
                               'medium': 'medium.a',
                               'large': 'large.a'
                           },
                           'scenes': [
                                {
                                    'id': 1,
                                    'title': 'B',
                                    'description': 'some',
                                    'picture': {
                                        'small': 'small.b',
                                        'medium': 'medium.b',
                                        'large': 'large.b',
                                    },
                                    'latitude': 1.2,
                                    'longitude': -3.4,
                                    'experience_id': 1,
                                },
                                {
                                    'id': 2,
                                    'title': 'C',
                                    'description': 'other',
                                    'picture': {
                                        'small': 'small.c',
                                        'medium': 'medium.c',
                                        'large': 'large.c',
                                    },
                                    'latitude': 5.6,
                                    'longitude': -7.8,
                                    'experience_id': 1,
                                }
                           ]
                       }


def reset_imports_and_set_factories_module(factories_mock):
    if 'experiences.factories' in sys.modules:
        del(sys.modules['experiences.factories'])
    if 'experiences.views' in sys.modules:
        del(sys.modules['experiences.views'])
    sys.modules['experiences.factories'] = factories_mock
