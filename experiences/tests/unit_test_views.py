from mock import Mock

from abidria.entities import Picture
from abidria.exceptions import InvalidEntityException, EntityDoesNotExist
from experiences.entities import Experience
from experiences.views import ExperiencesView, ExperienceView


class TestExperiencesView(object):

    def test_returns_experiences_serialized_and_200(self):
        picture_a = Picture(small_url='small.a', medium_url='medium.a', large_url='large.a')
        experience_a = Experience(id=1, title='A', description='some', picture=picture_a)
        picture_b = Picture(small_url='small.b', medium_url='medium.b', large_url='large.b')
        experience_b = Experience(id=2, title='B', description='other', picture=picture_b)

        interactor_mock = Mock()
        interactor_mock.execute.return_value = [experience_a, experience_b]

        body, status = ExperiencesView(get_all_experiences_interactor=interactor_mock).get()

        assert status == 200
        assert body == [
                           {
                               'id': '1',
                               'title': 'A',
                               'description': 'some',
                               'picture': {'small_url': 'small.a',
                                           'medium_url': 'medium.a',
                                           'large_url': 'large.a'}
                           },
                           {
                               'id': '2',
                               'title': 'B',
                               'description': 'other',
                               'picture': {'small_url': 'small.b',
                                           'medium_url': 'medium.b',
                                           'large_url': 'large.b'}
                           },
                       ]

    def test_post_returns_experience_serialized_and_200(self):
        experience = Experience(id='1', title='B', description='some')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = experience

        view = ExperiencesView(create_new_experience_interactor=interactor_mock)
        body, status = view.post(title='B', description='some')

        interactor_mock.set_params.assert_called_once_with(title='B', description='some')
        assert status == 201
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                       }

    def test_post_returns_error_serialized_and_422(self):
        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.side_effect = \
            InvalidEntityException(source='title', code='empty_attribute', message='Title must not be empty.')

        view = ExperiencesView(create_new_experience_interactor=interactor_mock)
        body, status = view.post(title='B', description='some')

        assert status == 422
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'empty_attribute',
                                        'message': 'Title must not be empty.',
                                    }
                       }


class TestExperienceView(object):

    def test_patch_returns_experience_serialized_and_200(self):
        experience = Experience(id='1', title='B', description='some')

        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.return_value = experience

        view = ExperienceView(modify_experience_interactor=interactor_mock)
        body, status = view.patch(experience_id='1', description='some')

        interactor_mock.set_params.assert_called_once_with(id='1', title=None, description='some')
        assert status == 200
        assert body == {
                           'id': '1',
                           'title': 'B',
                           'description': 'some',
                           'picture': None,
                       }

    def test_patch_returns_error_serialized_and_422(self):
        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.side_effect = \
            InvalidEntityException(source='title', code='empty_attribute', message='Title must not be empty')

        view = ExperienceView(modify_experience_interactor=interactor_mock)
        body, status = view.patch(experience_id='1')

        assert status == 422
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'empty_attribute',
                                        'message': 'Title must not be empty',
                                    }
                       }

    def test_patch_returns_not_exists_error_serialized_and_404(self):
        interactor_mock = Mock()
        interactor_mock.set_params.return_value = interactor_mock
        interactor_mock.execute.side_effect = EntityDoesNotExist

        view = ExperienceView(modify_experience_interactor=interactor_mock)
        body, status = view.patch(experience_id='33')

        assert status == 404
        assert body == {
                           'error': {
                                        'source': 'entity',
                                        'code': 'not_found',
                                        'message': 'Entity not found',
                                    }
                       }
