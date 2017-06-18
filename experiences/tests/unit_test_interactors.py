from mock import Mock

from experiences.entities import Experience
from experiences.interactors import GetAllExperiences, GetExperience


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        experience_a = Experience(id=1, title='A', description='some', picture=None)
        experience_b = Experience(id=2, title='B', description='other', picture=None)
        experiences_repo = Mock()
        experiences_repo.get_all_experiences = Mock(return_value=[experience_a, experience_b])

        response = GetAllExperiences(experiences_repo).execute()

        assert response == [experience_a, experience_b]


class TestGetExperience(object):

    def test_returns_repo_response(self):
        experience_a = Experience(id=1, title='A', description='some', picture=None)
        experiences_repo = Mock()
        experiences_repo.get_experience = Mock(return_value=experience_a)

        response = GetExperience(experiences_repo).set_params(id=1).execute()

        experiences_repo.get_experience.assert_called_once_with(id=1)
        assert response == experience_a
