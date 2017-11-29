from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException
from scenes.validators import SceneValidator
from scenes.entities import Scene


class TestSceneValidator(object):

    def test_valid_scene_returns_true(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene() \
                .when_scene_is_validated() \
                .then_response_should_be_true()

    def test_no_title_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(title=None) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='title', code='empty_attribute',
                                            message='Title cannot be empty')

    def test_wrong_type_title_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(title=1) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='title', code='wrong_type',
                                            message='Title must be string')

    def test_void_title_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(title='') \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='title', code='wrong_size',
                                            message='Title must be between 1 and 30 chars')

    def test_large_title_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(title='*'*31) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='title', code='wrong_size',
                                            message='Title must be between 1 and 30 chars')

    def test_wrong_type_description_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(description=1) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='description', code='wrong_type',
                                            message='Description must be string')

    def test_no_latitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(latitude=None) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='latitude', code='empty_attribute',
                                            message='Latitude cannot be empty')

    def test_wrong_type_latitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(latitude='string') \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='latitude', code='wrong_type',
                                            message='Latitude must be numeric')

    def test_short_latitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(latitude=-90.00001) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='latitude', code='wrong_size',
                                            message='Latitude must be between -90 and +90')

    def test_large_latitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(latitude=90.00001) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='latitude', code='wrong_size',
                                            message='Latitude must be between -90 and +90')

    def test_no_longitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(longitude=None) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='longitude', code='empty_attribute',
                                            message='Longitude cannot be empty')

    def test_wrong_type_longitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(longitude='string') \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='longitude', code='wrong_type',
                                            message='Longitude must be numeric')

    def test_short_longitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(longitude=-180.00001) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='longitude', code='wrong_size',
                                            message='Longitude must be between -180 and +180')

    def test_large_longitude_scene_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(longitude=180.00001) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='longitude', code='wrong_size',
                                            message='Longitude must be between -180 and +180')

    def test_empty_experience_id_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene(experience_id=None) \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='experience_id', code='empty_attribute',
                                            message='Experience id cannot be empty')

    def test_unexistent_experience_id_returns_error(self):
        TestSceneValidator._ScenarioMaker() \
                .given_an_scene() \
                .given_an_unexistent_experience() \
                .when_scene_is_validated() \
                .then_error_should_be_raise(source='experience_id', code='does_not_exist',
                                            message='Experience does not exist')

    class _ScenarioMaker(object):

        def __init__(self):
            self._experience_repo = Mock()
            self._experience_repo.get_experience.return_value = True
            self._scene = None
            self._response = None
            self._error = None

        def given_an_unexistent_experience(self):
            self._experience_repo.get_experience.side_effect = EntityDoesNotExistException()
            return self

        def given_an_scene(self, title='Valid Title', description=None, latitude=1, longitude=1, experience_id=1):
            scene = Scene(title=title, description=description,
                          latitude=latitude, longitude=longitude, experience_id=experience_id)
            self._scene = scene
            return self

        def when_scene_is_validated(self):
            validator = SceneValidator(self._experience_repo)
            try:
                self._response = validator.validate_scene(self._scene)
            except InvalidEntityException as e:
                self._error = e
            return self

        def then_response_should_be_true(self):
            assert self._response is True
            return self

        def then_error_should_be_raise(self, source=None, code=None, message=None):
            assert self._error.source == source
            assert self._error.code == code
            assert str(self._error) == message
            return self
