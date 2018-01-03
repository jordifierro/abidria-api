from mock import Mock

from abidria.entities import Picture
from experiences.entities import Experience
from experiences.views import ExperiencesView, ExperienceView, UploadExperiencePictureView, SaveExperienceView
from experiences.serializers import ExperienceSerializer, MultipleExperiencesSerializer
from experiences.interactors import SaveUnsaveExperienceInteractor


class TestExperiencesView(object):

    def test_returns_experiences_serialized_and_200(self):
        TestExperiencesView.ScenarioMaker() \
                .given_an_experience_a() \
                .given_an_experience_b() \
                .given_an_interactor_that_returns_that_experiences() \
                .when_get_experiences(logged_person_id='9', mine='false', saved='false') \
                .then_should_call_interactor_set_params(logged_person_id='9', mine=False, saved=False) \
                .then_status_code_should_be_200() \
                .then_response_body_should_be_experiences_serialized()

    def test_mine_returns_experiences_serialized_and_200(self):
        TestExperiencesView.ScenarioMaker() \
                .given_an_experience_a() \
                .given_an_experience_b() \
                .given_an_interactor_that_returns_that_experiences() \
                .when_get_experiences(logged_person_id='9', mine='true', saved='false') \
                .then_should_call_interactor_set_params(logged_person_id='9', mine=True, saved=False) \
                .then_status_code_should_be_200() \
                .then_response_body_should_be_experiences_serialized()

    def test_saved_returns_experiences_serialized_and_200(self):
        TestExperiencesView.ScenarioMaker() \
                .given_an_experience_a() \
                .given_an_experience_b() \
                .given_an_interactor_that_returns_that_experiences() \
                .when_get_experiences(logged_person_id='9', mine='false', saved='true') \
                .then_should_call_interactor_set_params(logged_person_id='9', mine=False, saved=True) \
                .then_status_code_should_be_200() \
                .then_response_body_should_be_experiences_serialized()

    class ScenarioMaker(object):

        def given_an_experience_a(self):
            picture_a = Picture(small_url='small.a', medium_url='medium.a', large_url='large.a')
            self.experience_a = Experience(id=1, title='A', description='some', picture=picture_a,
                                           author_id='4', author_username='usr')
            return self

        def given_an_experience_b(self):
            picture_b = Picture(small_url='small.b', medium_url='medium.b', large_url='large.b')
            self.experience_b = Experience(id=2, title='B', description='other', picture=picture_b,
                                           author_id='5', author_username='nms')
            return self

        def given_an_interactor_that_returns_that_experiences(self):
            self.interactor_mock = Mock()
            self.interactor_mock.set_params.return_value = self.interactor_mock
            self.interactor_mock.execute.return_value = [self.experience_a, self.experience_b]
            return self

        def when_get_experiences(self, logged_person_id, mine, saved):
            self.body, self.status = ExperiencesView(get_all_experiences_interactor=self.interactor_mock) \
                    .get(logged_person_id=logged_person_id, mine=mine, saved=saved)
            return self

        def then_should_call_interactor_set_params(self, logged_person_id, mine, saved):
            self.interactor_mock.set_params.assert_called_once_with(logged_person_id=logged_person_id,
                                                                    mine=mine, saved=saved)
            return self

        def then_status_code_should_be_200(self):
            assert self.status == 200
            return self

        def then_response_body_should_be_experiences_serialized(self):
            assert self.body == MultipleExperiencesSerializer.serialize([self.experience_a, self.experience_b])
            return self

    def test_post_returns_experience_serialized_and_200(self):
        experience = Experience(id='1', title='B', description='some', author_id='6', author_username='usr')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = experience

        view = ExperiencesView(create_new_experience_interactor=interactor_mock)
        body, status = view.post(title='B', description='some', logged_person_id='7')

        interactor_mock.set_params.assert_called_once_with(title='B', description='some', logged_person_id='7')
        assert status == 201
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                           'author_id': '6',
                           'author_username': 'usr',
                           'is_mine': False,
                           'is_saved': False
                       }


class TestExperienceView(object):

    def test_patch_returns_experience_serialized_and_200(self):
        experience = Experience(id='1', title='B', description='some', author_id='8', author_username='usrnm')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = experience

        view = ExperienceView(modify_experience_interactor=interactor_mock)
        body, status = view.patch(experience_id='1', description='some', logged_person_id='5')

        interactor_mock.set_params.assert_called_once_with(id='1', title=None, description='some', logged_person_id='5')
        assert status == 200
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                           'author_id': '8',
                           'author_username': 'usrnm',
                           'is_mine': False,
                           'is_saved': False
                       }


class TestUploadExperiencePictureView(object):

    def test_post_returns_experience_serialized_and_200(self):
        TestUploadExperiencePictureView._ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience() \
                .given_an_interactor_that_returns_that_experience() \
                .given_an_id() \
                .given_a_picture() \
                .when_post_is_called() \
                .then_interactor_receives_params() \
                .then_response_status_is_200() \
                .then_response_body_is_experience_serialized()

    class _ScenarioMaker(object):

        def __init__(self):
            self._interactor_mock = Mock()
            self._interactor_mock.set_params.return_value = self._interactor_mock
            self._experience = None
            self._id = None
            self._picture = None
            self._response = None
            self._logged_person_id = None

        def given_a_logged_person_id(self):
            self._logged_person_id = '5'
            return self

        def given_an_experience(self):
            self._experience = Experience(id='1', title='B', description='some', author_id='3')
            return self

        def given_an_interactor_that_returns_that_experience(self):
            self._interactor_mock.execute.return_value = self._experience
            return self

        def given_an_id(self):
            self._id = '2'
            return self

        def given_a_picture(self):
            self._picture = 'pic'
            return self

        def when_post_is_called(self):
            view = UploadExperiencePictureView(upload_experience_picture_interactor=self._interactor_mock)
            self._body, self._status = view.post(experience_id=self._id, picture=self._picture,
                                                 logged_person_id=self._logged_person_id)
            return self

        def then_interactor_receives_params(self):
            self._interactor_mock.set_params.assert_called_once_with(experience_id=self._id, picture=self._picture,
                                                                     logged_person_id=self._logged_person_id)
            return self

        def then_response_status_is_200(self):
            assert self._status == 200
            return self

        def then_response_body_is_experience_serialized(self):
            assert self._body == ExperienceSerializer.serialize(self._experience)


class TestSaveExperienceView(object):

    def test_post_returns_201(self):
        TestSaveExperienceView.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience_id() \
                .given_an_interactor_that_returns_true() \
                .when_post_is_called() \
                .then_interactor_receives_params_and_action_SAVE() \
                .then_response_status_is_201()

    def test_delete_returns_204(self):
        TestSaveExperienceView.ScenarioMaker() \
                .given_a_logged_person_id() \
                .given_an_experience_id() \
                .given_an_interactor_that_returns_true() \
                .when_delete_is_called() \
                .then_interactor_receives_params_and_action_UNSAVE() \
                .then_response_status_is_204()

    class ScenarioMaker(object):

        def given_a_logged_person_id(self):
            self.logged_person_id = '5'
            return self

        def given_an_experience_id(self):
            self.experience_id = '6'
            return self

        def given_an_interactor_that_returns_true(self):
            self.interactor_mock = Mock()
            self.interactor_mock.execute.return_value = True
            return self

        def when_post_is_called(self):
            view = SaveExperienceView(save_unsave_experience_interactor=self.interactor_mock)
            self.body, self.status = view.post(experience_id=self.experience_id, logged_person_id=self.logged_person_id)
            return self

        def when_delete_is_called(self):
            view = SaveExperienceView(save_unsave_experience_interactor=self.interactor_mock)
            self.body, self.status = view.delete(experience_id=self.experience_id,
                                                 logged_person_id=self.logged_person_id)
            return self

        def then_interactor_receives_params_and_action_SAVE(self):
            self.interactor_mock.set_params.assert_called_once_with(action=SaveUnsaveExperienceInteractor.Action.SAVE,
                                                                    experience_id=self.experience_id,
                                                                    logged_person_id=self.logged_person_id)
            return self

        def then_interactor_receives_params_and_action_UNSAVE(self):
            self.interactor_mock.set_params.assert_called_once_with(action=SaveUnsaveExperienceInteractor.Action.UNSAVE,
                                                                    experience_id=self.experience_id,
                                                                    logged_person_id=self.logged_person_id)
            return self

        def then_response_status_is_204(self):
            assert self.status == 204
            return self

        def then_response_status_is_201(self):
            assert self.status == 201
            return self
