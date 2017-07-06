import sys
from decimal import Decimal

from mock import Mock

from abidria.entities import Picture
from scenes.entities import Scene


class TestScenesDetailView(object):

    def test_returns_scenes_serialized_and_200(self):
        picture_b = Picture(small='small.b', medium='medium.b', large='large.b')
        picture_c = Picture(small='small.c', medium='medium.c', large='large.c')
        scene_b = Scene(id=1, title='B', description='some', picture=picture_b,
                        latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id=1)
        scene_c = Scene(id=2, title='C', description='other', picture=picture_c,
                        latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=1)

        get_scenes_mock = Mock()
        get_scenes_mock.set_params = Mock(return_value=get_scenes_mock)
        get_scenes_mock.execute = Mock(return_value=[scene_b, scene_c])

        factories_mock = Mock()
        factories_mock.GetScenesFromExperienceFactory.get = Mock(return_value=get_scenes_mock)
        reset_imports_and_set_factories_module(factories_mock)
        from scenes.views import ScenesView

        body, status = ScenesView().get(experience='1')

        get_scenes_mock.set_params.assert_called_once_with(experience_id='1')
        assert status == 200
        assert body == [
                           {
                               'id': '1',
                               'title': 'B',
                               'description': 'some',
                               'picture': {
                                   'small': 'small.b',
                                   'medium': 'medium.b',
                                   'large': 'large.b',
                               },
                               'latitude': 1.2,
                               'longitude': -3.4,
                               'experience_id': '1',
                           },
                           {
                               'id': '2',
                               'title': 'C',
                               'description': 'other',
                               'picture': {
                                   'small': 'small.c',
                                   'medium': 'medium.c',
                                   'large': 'large.c',
                               },
                               'latitude': 5.6,
                               'longitude': -7.8,
                               'experience_id': '1',
                           }
                       ]


def reset_imports_and_set_factories_module(factories_mock):
    if 'scenes.factories' in sys.modules:
        del(sys.modules['scenes.factories'])
    if 'scenes.views' in sys.modules:
        del(sys.modules['scenes.views'])
    sys.modules['scenes.factories'] = factories_mock
