from mock import Mock

from experiences.entities import Experience
from experiences.interactors import GetAllExperiences, GetExperience
from scenes.entities import Scene


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        experience_a = Experience(id=1, title='A', description='some', picture=None)
        experience_b = Experience(id=2, title='B', description='other', picture=None)
        experiences_repo = Mock()
        experiences_repo.get_all_experiences = Mock(return_value=[experience_a, experience_b])

        response = GetAllExperiences(experiences_repo).execute()

        assert response == [experience_a, experience_b]


class TestGetExperience(object):

    def test_returns_experience_and_its_scenes(self):
        experience_a = Experience(id=1, title='A', description='some', picture=None)
        experience_repo = Mock()
        experience_repo.get_experience = Mock(return_value=experience_a)

        scene_a = Scene(id=2)
        scene_b = Scene(id=3)
        scene_repo = Mock()
        scene_repo.get_scenes = Mock(return_value=[scene_a, scene_b])

        response = GetExperience(experience_repo, scene_repo).set_params(id=1).execute()

        experience_repo.get_experience.assert_called_once_with(id=1)
        scene_repo.get_scenes.assert_called_once_with(experience_id=1)
        assert response == (experience_a, [scene_a, scene_b])
