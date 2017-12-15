from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException
from scenes.interactors import GetScenesFromExperienceInteractor, CreateNewSceneInteractor, ModifySceneInteractor
from scenes.entities import Scene


class TestGetScenesFromExperience(object):

    def test_returns_scenes(self):
        TestGetScenesFromExperience.ScenarioMaker() \
                .given_two_scenes() \
                .given_scene_repo_that_returns_both() \
                .given_an_experience_id() \
                .when_interactor_is_executed() \
                .then_get_scenes_should_be_called_with_experience_id() \
                .then_result_should_be_both_scenes()

    class ScenarioMaker(object):

        def given_two_scenes(self):
            self.scene_a = Scene(id=2, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
            self.scene_b = Scene(id=3, title='', description='', picture=None, latitude=1, longitude=0, experience_id=1)
            return self

        def given_scene_repo_that_returns_both(self):
            self.scene_repo = Mock()
            self.scene_repo.get_scenes.return_value = [self.scene_a, self.scene_b]
            return self

        def given_an_experience_id(self):
            self.experience_id = '5'
            return self

        def when_interactor_is_executed(self):
            self.result = GetScenesFromExperienceInteractor(self.scene_repo) \
                    .set_params(experience_id=self.experience_id).execute()
            return self

        def then_get_scenes_should_be_called_with_experience_id(self):
            self.scene_repo.get_scenes.assert_called_once_with(experience_id=self.experience_id)
            return self

        def then_result_should_be_both_scenes(self):
            assert self.result == [self.scene_a, self.scene_b]
            return self


class TestCreateNewScene(object):

    def test_creates_and_returns_scene(self):
        TestCreateNewScene.ScenarioMaker() \
                .given_a_title() \
                .given_a_description() \
                .given_a_latitude() \
                .given_a_longitude() \
                .given_an_experience_id() \
                .given_an_scene_validator_that_accepts_that_scene() \
                .given_an_scene() \
                .given_an_scene_repo_that_returns_scene_on_create() \
                .when_interactor_is_executed() \
                .then_validate_scene_is_called_with_previous_params() \
                .then_create_scene_is_called_with_previous_params() \
                .then_result_should_be_scene()

    def test_invalid_scene_returns_error_and_doesnt_create_it(self):
        TestCreateNewScene.ScenarioMaker() \
                .given_a_title() \
                .given_a_description() \
                .given_a_latitude() \
                .given_a_longitude() \
                .given_an_experience_id() \
                .given_an_scene_validator_that_raises_invalid_params() \
                .given_an_scene_repo() \
                .when_interactor_is_executed() \
                .then_validate_scene_is_called_with_previous_params() \
                .then_create_scene_should_not_be_called() \
                .then_should_raise_invalid_entity_exception()

    class ScenarioMaker(object):

        def given_a_title(self):
            self.title = 'Title'
            return self

        def given_a_description(self):
            self.description = 'description'
            return self

        def given_a_latitude(self):
            self.latitude = 1
            return self

        def given_a_longitude(self):
            self.longitude = 0
            return self

        def given_an_experience_id(self):
            self.experience_id = '9'
            return self

        def given_an_scene(self):
            self.created_scene = Scene(title='Title', description='', latitude=1, longitude=0, experience_id=1)
            return self

        def given_an_scene_validator_that_accepts_that_scene(self):
            self.scene_validator = Mock()
            self.scene_validator.validate_scene.return_value = True
            return self

        def given_an_scene_validator_that_raises_invalid_params(self):
            self.scene_validator = Mock()
            self.scene_validator.validate_scene.side_effect = InvalidEntityException(source='s', code='c', message='m')
            return self

        def given_an_scene_repo_that_returns_scene_on_create(self):
            self.scene_repo = Mock()
            self.scene_repo.create_scene.return_value = self.created_scene
            return self

        def given_an_scene_repo(self):
            self.scene_repo = Mock()
            return self

        def when_interactor_is_executed(self):
            try:
                self.result = CreateNewSceneInteractor(self.scene_repo, self.scene_validator) \
                    .set_params(title=self.title, description=self.description, latitude=self.latitude,
                                longitude=self.longitude, experience_id=self.experience_id).execute()
            except Exception as e:
                self.error = e
            return self

        def then_validate_scene_is_called_with_previous_params(self):
            scene = Scene(title=self.title, description=self.description, latitude=self.latitude,
                          longitude=self.longitude, experience_id=self.experience_id)
            self.scene_validator.validate_scene.assert_called_once_with(scene)
            return self

        def then_create_scene_is_called_with_previous_params(self):
            scene = Scene(title=self.title, description=self.description, latitude=self.latitude,
                          longitude=self.longitude, experience_id=self.experience_id)
            self.scene_repo.create_scene.assert_called_once_with(scene)
            return self

        def then_create_scene_should_not_be_called(self):
            self.scene_repo.created_scene.assert_not_called()
            return self

        def then_result_should_be_scene(self):
            assert self.result == self.created_scene

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 's'
            assert self.error.code == 'c'
            assert str(self.error) == 'm'
            return self


class TestModifyScene(object):

    def test_gets_modifies_not_none_params_and_returns_scene(self):
        TestModifyScene.ScenarioMaker() \
                .given_an_scene() \
                .given_an_scene_repo() \
                .given_that_scene_repo_returns_that_scene_on_get() \
                .given_an_updated_scene() \
                .given_that_scene_repo_returns_that_scene_on_update() \
                .given_an_scene_validator_that_accepts() \
                .given_an_id() \
                .given_a_description() \
                .given_a_longitude() \
                .when_interactor_is_executed() \
                .then_get_scene_should_be_called_with_id() \
                .then_scene_with_new_description_an_longitude_should_be_validated() \
                .then_update_scene_should_be_called_with_new_description_an_longitude() \
                .then_result_should_be_updated_scene()

    def test_invalid_scene_returns_error_and_doesnt_update_it(self):
        TestModifyScene.ScenarioMaker() \
                .given_an_scene() \
                .given_an_scene_repo() \
                .given_that_scene_repo_returns_that_scene_on_get() \
                .given_an_scene_validator_that_raises_invalid_params() \
                .given_an_id() \
                .given_a_description() \
                .given_a_longitude() \
                .when_interactor_is_executed() \
                .then_get_scene_should_be_called_with_id() \
                .then_scene_with_new_description_an_longitude_should_be_validated() \
                .then_update_scene_should_not_be_called() \
                .then_should_raise_invalid_entity_exception()

    def test_unexistent_scene_returns_entity_does_not_exist_error(self):
        TestModifyScene.ScenarioMaker() \
                .given_an_scene_repo_that_raises_entity_does_not_exist() \
                .given_an_scene_validator_that_raises_invalid_params() \
                .given_an_id() \
                .given_a_description() \
                .given_a_longitude() \
                .when_interactor_is_executed() \
                .then_get_scene_should_be_called_with_id() \
                .then_update_scene_should_not_be_called() \
                .then_should_raise_entity_does_not_exist()

    class ScenarioMaker(object):

        def given_an_scene(self):
            self.scene = Scene(id='1', title='Title', description='some', latitude=1, longitude=0, experience_id=1)
            return self

        def given_an_scene_repo(self):
            self.scene_repo = Mock()
            return self

        def given_an_scene_repo_that_raises_entity_does_not_exist(self):
            self.scene_repo = Mock()
            self.scene_repo.get_scene.side_effect = EntityDoesNotExistException()
            return self

        def given_that_scene_repo_returns_that_scene_on_get(self):
            self.scene_repo.get_scene.return_value = self.scene
            return self

        def given_an_updated_scene(self):
            self.updated_scene = Scene(id='2', title='T', description='s', latitude=2, longitude=8, experience_id=1)
            return self

        def given_that_scene_repo_returns_that_scene_on_update(self):
            self.scene_repo.update_scene.return_value = self.updated_scene
            return self

        def given_an_scene_validator_that_accepts(self):
            self.scene_validator = Mock()
            self.scene_validator.validate_scene.return_value = True
            return self

        def given_an_scene_validator_that_raises_invalid_params(self):
            self.scene_validator = Mock()
            self.scene_validator.validate_scene.side_effect = InvalidEntityException(source='s', code='c', message='m')
            return self

        def given_an_id(self):
            self.id = '6'
            return self

        def given_a_description(self):
            self.description = 'description'
            return self

        def given_a_longitude(self):
            self.longitude = 0
            return self

        def when_interactor_is_executed(self):
            try:
                self.result = ModifySceneInteractor(self.scene_repo, self.scene_validator) \
                    .set_params(id=self.id, title=None, description=self.description, latitude=None,
                                longitude=self.longitude, experience_id=1).execute()
            except Exception as e:
                self.error = e
            return self

        def then_get_scene_should_be_called_with_id(self):
            self.scene_repo.get_scene.assert_called_once_with(id=self.id)
            return self

        def then_scene_with_new_description_an_longitude_should_be_validated(self):
            new_scene = Scene(id=self.scene.id, title=self.scene.title, description=self.description,
                              latitude=self.scene.latitude, longitude=self.longitude,
                              experience_id=self.scene.experience_id)
            self.scene_validator.validate_scene.assert_called_once_with(new_scene)
            return self

        def then_update_scene_should_be_called_with_new_description_an_longitude(self):
            new_scene = Scene(id=self.scene.id, title=self.scene.title, description=self.description,
                              latitude=self.scene.latitude, longitude=self.longitude,
                              experience_id=self.scene.experience_id)
            self.scene_repo.update_scene.assert_called_once_with(new_scene)
            return self

        def then_result_should_be_updated_scene(self):
            assert self.result == self.updated_scene
            return self

        def then_update_scene_should_not_be_called(self):
            self.scene_repo.update_scene.assert_not_called()
            return self

        def then_should_raise_invalid_entity_exception(self):
            assert type(self.error) is InvalidEntityException
            assert self.error.source == 's'
            assert self.error.code == 'c'
            assert str(self.error) == 'm'
            return self

        def then_should_raise_entity_does_not_exist(self):
            assert type(self.error) is EntityDoesNotExistException
            return self
