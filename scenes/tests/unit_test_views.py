from decimal import Decimal

from mock import Mock

from abidria.entities import Picture
from scenes.entities import Scene
from scenes.views import ScenesView, SceneView, UploadScenePictureView
from scenes.serializers import SceneSerializer, MultipleScenesSerializer


class TestScenesView:

    def test_get_returns_scenes_serialized_and_200(self):
        TestScenesView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_scene() \
                .given_another_scene() \
                .given_an_interactor_that_returns_both_scenes() \
                .given_an_experience_id() \
                .when_get_is_called_with_this_experience_id() \
                .then_interactor_is_called_with_experience_id() \
                .then_response_status_is_200() \
                .then_response_body_are_scenes_serialized()

    def test_post_returns_scene_serialized_and_200(self):
        TestScenesView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_scene() \
                .given_an_interactor_that_returns_that_scene() \
                .given_a_title() \
                .given_a_description() \
                .given_a_latitude() \
                .given_a_longitude() \
                .given_an_experience_id() \
                .when_post_is_called_with_these_params() \
                .then_interactor_receives_these_params() \
                .then_response_status_is_201() \
                .then_response_body_is_scene_serialized()

    class _ScenarioMaker:

        def __init__(self):
            self._interactor_mock = Mock()
            self._interactor_mock.set_params.return_value = self._interactor_mock
            self._scene = None
            self._title = None
            self._description = None
            self._latitude = None
            self._longitude = None
            self._experience_id = None
            self._response = None

        def given_a_logged_person_id(self):
            self.logged_person_id = '5'
            return self

        def given_an_scene(self):
            pic = Picture(small_url='small.b', medium_url='medium.b', large_url='large.b')
            self._scene = Scene(id='1', title='B', description='some', picture=pic,
                                latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id='1')
            return self

        def given_another_scene(self):
            pic = Picture(small_url='small.c', medium_url='medium.c', large_url='large.c')
            self._second_scene = Scene(id=2, title='C', description='other', picture=pic,
                                       latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=1)
            return self

        def given_an_interactor_that_returns_that_scene(self):
            self._interactor_mock.execute.return_value = self._scene
            return self

        def given_an_interactor_that_returns_both_scenes(self):
            self._interactor_mock.execute.return_value = [self._scene, self._second_scene]
            return self

        def given_a_title(self):
            self._title = 'TTtt'
            return self

        def given_a_description(self):
            self._description = 'any'
            return self

        def given_a_latitude(self):
            self._latitude = Decimal('-0.9')
            return self

        def given_a_longitude(self):
            self._longitude = Decimal('-4.1')
            return self

        def given_an_experience_id(self):
            self._experience_id = '4'
            return self

        def when_post_is_called_with_these_params(self):
            view = ScenesView(create_new_scene_interactor=self._interactor_mock)
            self._body, self._status = view.post(title=self._title, description=self._description,
                                                 latitude=self._latitude, longitude=self._longitude,
                                                 experience_id=self._experience_id,
                                                 logged_person_id=self.logged_person_id)
            return self

        def when_get_is_called_with_this_experience_id(self):
            view = ScenesView(get_scenes_from_experience_interactor=self._interactor_mock)
            self._body, self._status = view.get(experience=self._experience_id, logged_person_id=self.logged_person_id)
            return self

        def then_interactor_is_called_with_experience_id(self):
            self._interactor_mock.set_params.assert_called_once_with(experience_id=self._experience_id,
                                                                     logged_person_id=self.logged_person_id)
            return self

        def then_interactor_receives_these_params(self):
            self._interactor_mock.set_params.assert_called_once_with(title=self._title, description=self._description,
                                                                     latitude=float(self._latitude),
                                                                     longitude=float(self._longitude),
                                                                     experience_id=self._experience_id,
                                                                     logged_person_id=self.logged_person_id)
            return self

        def then_response_status_is_200(self):
            assert self._status == 200
            return self

        def then_response_status_is_201(self):
            assert self._status == 201
            return self

        def then_response_body_is_scene_serialized(self):
            assert self._body == SceneSerializer.serialize(self._scene)
            return self

        def then_response_body_are_scenes_serialized(self):
            assert self._body == MultipleScenesSerializer.serialize([self._scene, self._second_scene])
            return self


class TestSceneView:

    def test_patch_returns_scene_serialized_and_200(self):
        TestSceneView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_scene() \
                .given_an_interactor_that_returns_that_scene() \
                .given_an_id() \
                .given_a_description() \
                .given_a_longitude() \
                .when_patch_is_called_with_id_description_longitude_and_logged_person_id() \
                .then_interactor_receives_params_id_description_longitude_and_logged_person_id() \
                .then_response_status_is_200() \
                .then_response_body_is_scene_serialized()

    class _ScenarioMaker:

        def __init__(self):
            self._interactor_mock = Mock()
            self._interactor_mock.set_params.return_value = self._interactor_mock
            self._scene = None
            self._id = None
            self._description = None
            self._longitude = None
            self._response = None
            self._logged_person_id = None

        def given_a_logged_person_id(self):
            self._logged_person_id = '5'
            return self

        def given_an_scene(self):
            self._scene = Scene(id='1', title='B', description='some',
                                latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id='1')
            return self

        def given_an_interactor_that_returns_that_scene(self):
            self._interactor_mock.execute.return_value = self._scene
            return self

        def given_an_id(self):
            self._id = '2'
            return self

        def given_a_description(self):
            self._description = 'any'
            return self

        def given_a_longitude(self):
            self._longitude = Decimal('-4.1')
            return self

        def when_patch_is_called_with_id_description_longitude_and_logged_person_id(self):
            view = SceneView(modify_scene_interactor=self._interactor_mock)
            self._body, self._status = view.patch(scene_id=self._id, description=self._description,
                                                  longitude=self._longitude, logged_person_id=self._logged_person_id)
            return self

        def then_interactor_receives_params_id_description_longitude_and_logged_person_id(self):
            self._interactor_mock.set_params.assert_called_once_with(id=self._id, title=None,
                                                                     description=self._description,
                                                                     latitude=None, longitude=float(self._longitude),
                                                                     experience_id=None,
                                                                     logged_person_id=self._logged_person_id)
            return self

        def then_response_status_is_200(self):
            assert self._status == 200
            return self

        def then_response_body_is_scene_serialized(self):
            assert self._body == SceneSerializer.serialize(self._scene)


class TestUploadScenePictureView:

    def test_post_returns_scene_serialized_and_200(self):
        TestUploadScenePictureView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_scene() \
                .given_an_interactor_that_returns_that_scene() \
                .given_an_id() \
                .given_a_picture() \
                .when_post_is_called() \
                .then_interactor_receives_params() \
                .then_response_status_is_200() \
                .then_response_body_is_scene_serialized()

    class _ScenarioMaker:

        def __init__(self):
            self._interactor_mock = Mock()
            self._interactor_mock.set_params.return_value = self._interactor_mock
            self._scene = None
            self._id = None
            self._picture = None
            self._response = None
            self._logged_person_id = None

        def given_a_logged_person_id(self):
            self._logged_person_id = '5'
            return self

        def given_an_scene(self):
            self._scene = Scene(id='1', title='B', description='some',
                                latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id='1')
            return self

        def given_an_interactor_that_returns_that_scene(self):
            self._interactor_mock.execute.return_value = self._scene
            return self

        def given_an_id(self):
            self._id = '2'
            return self

        def given_a_picture(self):
            self._picture = 'pic'
            return self

        def when_post_is_called(self):
            view = UploadScenePictureView(upload_scene_picture_interactor=self._interactor_mock)
            self._body, self._status = view.post(scene_id=self._id, picture=self._picture,
                                                 logged_person_id=self._logged_person_id)
            return self

        def then_interactor_receives_params(self):
            self._interactor_mock.set_params.assert_called_once_with(scene_id=self._id, picture=self._picture,
                                                                     logged_person_id=self._logged_person_id)
            return self

        def then_response_status_is_200(self):
            assert self._status == 200
            return self

        def then_response_body_is_scene_serialized(self):
            assert self._body == SceneSerializer.serialize(self._scene)
