from mock import Mock

from abidria.entities import Picture
from experiences.entities import Experience
from experiences.views import ExperiencesView, ExperienceView


class TestExperiencesView(object):

    def test_returns_experiences_serialized_and_200(self):
        picture_a = Picture(small_url='small.a', medium_url='medium.a', large_url='large.a')
        experience_a = Experience(id=1, title='A', description='some', picture=picture_a,
                                  author_id='4', author_username='usr')
        picture_b = Picture(small_url='small.b', medium_url='medium.b', large_url='large.b')
        experience_b = Experience(id=2, title='B', description='other', picture=picture_b,
                                  author_id='5', author_username='nms')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = [experience_a, experience_b]

        body, status = ExperiencesView(get_all_experiences_interactor=interactor_mock).get(logged_person_id='4')

        interactor_mock.set_params.assert_called_once_with(logged_person_id='4')
        assert status == 200
        assert body == [
                           {
                               'id': '1',
                               'title': 'A',
                               'description': 'some',
                               'picture': {'small_url': 'small.a',
                                           'medium_url': 'medium.a',
                                           'large_url': 'large.a'},
                               'author_id': '4',
                               'author_username': 'usr'
                           },
                           {
                               'id': '2',
                               'title': 'B',
                               'description': 'other',
                               'picture': {'small_url': 'small.b',
                                           'medium_url': 'medium.b',
                                           'large_url': 'large.b'},
                               'author_id': '5',
                               'author_username': 'nms'
                           },
                       ]

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
                           'author_username': 'usr'
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
                           'author_username': 'usrnm'
                       }
