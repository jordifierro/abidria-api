from mock import Mock

from abidria.exceptions import InvalidEntityException
from scenes.interactors import GetScenesFromExperienceInteractor, CreateNewSceneInteractor
from scenes.entities import Scene


class TestGetScenesFromExperience(object):

    def test_returns_scenes(self):
        scene_a = Scene(id=2, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
        scene_b = Scene(id=3, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
        scene_repo = Mock()
        scene_repo.get_scenes.return_value = [scene_a, scene_b]

        response = GetScenesFromExperienceInteractor(scene_repo).set_params(experience_id=1).execute()

        scene_repo.get_scenes.assert_called_once_with(experience_id=1)
        assert response == [scene_a, scene_b]


class TestCreateNewScene(object):

    def test_creates_and_returns_scene(self):
        scene = Scene(title='Title', description='', latitude=1, longitude=0, experience_id=1)
        scene_repo = Mock()
        scene_repo.save_scene.return_value = scene

        scene_validator = Mock()
        scene_validator.validate_scene.return_value = True

        response = CreateNewSceneInteractor(scene_repo, scene_validator) \
            .set_params(title='Title', description='', latitude=1, longitude=0, experience_id=1).execute()

        scene_repo.save_scene.assert_called_once_with(scene)
        scene_validator.validate_scene.assert_called_once_with(scene)
        assert response == scene

    def test_invalid_scene_returns_error_and_doesnt_create_it(self):
        scene = Scene(title='', description='', latitude=0, longitude=0, experience_id=0)
        scene_repo = Mock()
        scene_validator = Mock()
        scene_validator.validate_scene.side_effect = InvalidEntityException(source='s', code='c', message='m')

        try:
            CreateNewSceneInteractor(scene_repo, scene_validator) \
                .set_params(title='', description='', latitude=0, longitude=0, experience_id=0).execute()
            assert False
        except InvalidEntityException as invalid_exc:
            assert invalid_exc.source == 's'
            assert invalid_exc.code == 'c'
            assert str(invalid_exc) == 'm'
            scene_repo.save_scene.assert_not_called()
            scene_validator.validate_scene.assert_called_once_with(scene)
