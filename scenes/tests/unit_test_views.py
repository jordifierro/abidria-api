from decimal import Decimal

from mock import Mock

from abidria.entities import Picture
from scenes.entities import Scene
from scenes.views import ScenesView, SceneView


class TestScenesDetailView(object):

    def test_get_returns_scenes_serialized_and_200(self):
        picture_b = Picture(small_url='small.b', medium_url='medium.b', large_url='large.b')
        picture_c = Picture(small_url='small.c', medium_url='medium.c', large_url='large.c')
        scene_b = Scene(id=1, title='B', description='some', picture=picture_b,
                        latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id=1)
        scene_c = Scene(id=2, title='C', description='other', picture=picture_c,
                        latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=1)

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = [scene_b, scene_c]

        body, status = ScenesView(get_scenes_from_experience_interactor=interactor_mock).get(experience='1')

        interactor_mock.set_params.assert_called_once_with(experience_id='1')
        assert status == 200
        assert body == [
                           {
                               'id': '1',
                               'title': 'B',
                               'description': 'some',
                               'picture': {
                                   'small_url': 'small.b',
                                   'medium_url': 'medium.b',
                                   'large_url': 'large.b',
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
                                   'small_url': 'small.c',
                                   'medium_url': 'medium.c',
                                   'large_url': 'large.c',
                               },
                               'latitude': 5.6,
                               'longitude': -7.8,
                               'experience_id': '1',
                           }
                       ]

    def test_post_returns_scene_serialized_and_200(self):
        scene = Scene(id='1', title='B', description='some',
                      latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id='1')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = scene

        view = ScenesView(create_new_scene_interactor=interactor_mock)
        body, status = view.post(title='B', description='some', latitude=1.2, longitude=-3.4, experience_id='1')

        interactor_mock.set_params.assert_called_once_with(title='B', description='some',
                                                           latitude=1.2, longitude=-3.4, experience_id='1')
        assert status == 201
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                           'latitude': 1.2,
                           'longitude': -3.4,
                           'experience_id': '1'
                       }


class TestSceneView(object):

    def test_patch_returns_scene_serialized_and_200(self):
        scene = Scene(id='1', title='B', description='some',
                      latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id='1')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = scene

        view = SceneView(modify_scene_interactor=interactor_mock)
        body, status = view.patch(scene_id='1', description='some', longitude=-3.4)

        interactor_mock.set_params.assert_called_once_with(id='1', title=None, description='some',
                                                           latitude=None, longitude=-3.4, experience_id=None)
        assert status == 200
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                           'latitude': 1.2,
                           'longitude': -3.4,
                           'experience_id': '1'
                       }
