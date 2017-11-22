from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExist
from scenes.interactors import GetScenesFromExperienceInteractor, CreateNewSceneInteractor, ModifySceneInteractor
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
        scene_repo.create_scene.return_value = scene

        scene_validator = Mock()
        scene_validator.validate_scene.return_value = True

        response = CreateNewSceneInteractor(scene_repo, scene_validator) \
            .set_params(title='Title', description='', latitude=1, longitude=0, experience_id=1).execute()

        scene_repo.create_scene.assert_called_once_with(scene)
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
            scene_repo.create_scene.assert_not_called()
            scene_validator.validate_scene.assert_called_once_with(scene)


class TestModifyScene(object):

    def test_gets_modifies_not_none_params_and_returns_scene(self):
        scene = Scene(id='1', title='Title', description='some', latitude=1, longitude=0, experience_id=1)
        scene_repo = Mock()
        scene_repo.get_scene.return_value = scene

        updated_scene = Scene(id='1', title='Title', description='', latitude=1, longitude=8, experience_id=1)
        scene_repo.update_scene.return_value = updated_scene

        scene_validator = Mock()
        scene_validator.validate_scene.return_value = True

        response = ModifySceneInteractor(scene_repo, scene_validator) \
            .set_params(id='1', title=None, description='', latitude=None, longitude=8, experience_id=1).execute()

        scene_repo.get_scene.assert_called_once_with(id='1')
        scene_repo.update_scene.assert_called_once_with(updated_scene)
        scene_validator.validate_scene.assert_called_once_with(updated_scene)
        assert response == updated_scene

    def test_invalid_scene_returns_error_and_doesnt_update_it(self):
        scene = Scene(id='1', title='', description='', latitude=0, longitude=0, experience_id=0)
        scene_repo = Mock()
        scene_repo.get_scene.return_value = scene
        scene_validator = Mock()
        scene_validator.validate_scene.side_effect = InvalidEntityException(source='s', code='c', message='m')
        updated_scene = Scene(id='1', title='Other', description='some', latitude=3, longitude=8, experience_id=1)

        try:
            ModifySceneInteractor(scene_repo, scene_validator) \
                .set_params(id='1', title='Other', description='some',
                            latitude=3, longitude=8, experience_id=1).execute()
            assert False
        except InvalidEntityException as invalid_exc:
            assert invalid_exc.source == 's'
            assert invalid_exc.code == 'c'
            assert str(invalid_exc) == 'm'
            scene_repo.get_scene.assert_called_once_with(id='1')
            scene_repo.update_scene.assert_not_called()
            scene_validator.validate_scene.assert_called_once_with(updated_scene)

    def test_unexistent_scene_returns_entity_does_not_exist_error(self):
        scene_repo = Mock()
        scene_repo.get_scene.side_effect = EntityDoesNotExist
        scene_validator = Mock()

        try:
            ModifySceneInteractor(scene_repo, scene_validator) \
                .set_params(id='1', title='Other', description='some',
                            latitude=3, longitude=8, experience_id=1).execute()
            assert False
        except EntityDoesNotExist:
            pass
