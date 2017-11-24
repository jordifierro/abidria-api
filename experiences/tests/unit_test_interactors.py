from mock import Mock

from abidria.exceptions import InvalidEntityException
from experiences.entities import Experience
from experiences.interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        experience_a = Experience(id=1, title='A', description='some', picture=None)
        experience_b = Experience(id=2, title='B', description='other', picture=None)
        experiences_repo = Mock()
        experiences_repo.get_all_experiences = Mock(return_value=[experience_a, experience_b])

        response = GetAllExperiencesInteractor(experiences_repo).execute()

        assert response == [experience_a, experience_b]


class TestCreateNewExperience(object):

    def test_creates_and_returns_experience(self):
        experience = Experience(title='Title', description='')
        experience_repo = Mock()
        experience_repo.create_experience.return_value = experience

        experience_validator = Mock()
        experience_validator.validate_experience.return_value = True

        response = CreateNewExperienceInteractor(experience_repo, experience_validator) \
            .set_params(title='Title', description='').execute()

        experience_repo.create_experience.assert_called_once_with(experience)
        experience_validator.validate_experience.assert_called_once_with(experience)
        assert response == experience

    def test_invalid_experience_returns_error_and_doesnt_create_it(self):
        experience = Experience(title='', description='')
        experience_repo = Mock()
        experience_validator = Mock()
        experience_validator.validate_experience.side_effect = InvalidEntityException(source='s', code='c', message='m')

        try:
            CreateNewExperienceInteractor(experience_repo, experience_validator) \
                .set_params(title='', description='').execute()
            assert False
        except InvalidEntityException as invalid_exc:
            assert invalid_exc.source == 's'
            assert invalid_exc.code == 'c'
            assert str(invalid_exc) == 'm'
            experience_repo.create_experience.assert_not_called()
            experience_validator.validate_experience.assert_called_once_with(experience)
