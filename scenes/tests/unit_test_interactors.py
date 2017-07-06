from mock import Mock

from scenes.interactors import GetScenesFromExperience
from scenes.entities import Scene


class TestGetScenesFromExperience(object):

    def test_returns_scenes(self):
        scene_a = Scene(id=2, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
        scene_b = Scene(id=3, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
        scene_repo = Mock()
        scene_repo.get_scenes = Mock(return_value=[scene_a, scene_b])

        response = GetScenesFromExperience(scene_repo).set_params(experience_id=1).execute()

        scene_repo.get_scenes.assert_called_once_with(experience_id=1)
        assert response == [scene_a, scene_b]
