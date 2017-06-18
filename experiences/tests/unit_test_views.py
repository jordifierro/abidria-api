import sys

from mock import Mock

from experiences.entities import Experience, Picture


class TestExperiencesView(object):

    def test_returns_experiences_serialized_and_200(self):
        picture_a = Picture(small='small.a', medium='medium.a', large='large.a')
        experience_a = Experience(id=1, title='A', description='some', picture=picture_a)
        picture_b = Picture(small='small.b', medium='medium.b', large='large.b')
        experience_b = Experience(id=2, title='B', description='other', picture=picture_b)

        factories_mock = Mock()
        factories_mock.GetAllExperiencesFactory.get().execute = Mock(return_value=[experience_a, experience_b])
        sys.modules['experiences.factories'] = factories_mock
        from experiences.views import ExperiencesView

        body, status = ExperiencesView().get()

        assert status == 200
        assert body == [
                           {
                               'id': 1,
                               'title': 'A',
                               'description': 'some',
                               'picture': {'small': 'small.a',
                                           'medium': 'medium.a',
                                           'large': 'large.a'}
                           },
                           {
                               'id': 2,
                               'title': 'B',
                               'description': 'other',
                               'picture': {'small': 'small.b',
                                           'medium': 'medium.b',
                                           'large': 'large.b'}
                           },
                       ]
