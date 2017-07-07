from decimal import Decimal

from mock import Mock

from abidria.entities import Picture
from scenes.entities import Scene
from scenes.views import ScenesView


class TestScenesDetailView(object):

    def test_returns_scenes_serialized_and_200(self):
        picture_b = Picture(small='small.b', medium='medium.b', large='large.b')
        picture_c = Picture(small='small.c', medium='medium.c', large='large.c')
        scene_b = Scene(id=1, title='B', description='some', picture=picture_b,
                        latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id=1)
        scene_c = Scene(id=2, title='C', description='other', picture=picture_c,
                        latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=1)

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = [scene_b, scene_c]

        body, status = ScenesView(interactor_mock).get(experience='1')

        interactor_mock.set_params.assert_called_once_with(experience_id='1')
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
