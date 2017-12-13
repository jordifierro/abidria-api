from mock import Mock

from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException
from experiences.entities import Experience
from experiences.interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor, \
        ModifyExperienceInteractor


class TestGetAllExperiences(object):

    def test_returns_repo_response(self):
        experience_a = Experience(id=1, title='A', description='some',
                                  picture=None, author_id='1', author_username='usr')
        experience_b = Experience(id=2, title='B', description='other',
                                  picture=None, author_id='1', author_username='usr')
        experiences_repo = Mock()
        experiences_repo.get_all_experiences = Mock(return_value=[experience_a, experience_b])

        response = GetAllExperiencesInteractor(experiences_repo).execute()

        assert response == [experience_a, experience_b]


class TestCreateNewExperience(object):

    def test_creates_and_returns_experience(self):
        experience = Experience(title='Title', description='', author_id='3')
        experience_repo = Mock()
        experience_repo.create_experience.return_value = experience

        experience_validator = Mock()
        experience_validator.validate_experience.return_value = True

        response = CreateNewExperienceInteractor(experience_repo, experience_validator) \
            .set_params(title='Title', description='', logged_person_id='3').execute()

        experience_repo.create_experience.assert_called_once_with(experience)
        experience_validator.validate_experience.assert_called_once_with(experience)
        assert response == experience

    def test_invalid_experience_returns_error_and_doesnt_create_it(self):
        experience = Experience(title='', description='', author_id='')
        experience_repo = Mock()
        experience_validator = Mock()
        experience_validator.validate_experience.side_effect = InvalidEntityException(source='s', code='c', message='m')

        try:
            CreateNewExperienceInteractor(experience_repo, experience_validator) \
                .set_params(title='', description='', logged_person_id='').execute()
            assert False
        except InvalidEntityException as invalid_exc:
            assert invalid_exc.source == 's'
            assert invalid_exc.code == 'c'
            assert str(invalid_exc) == 'm'
            experience_repo.create_experience.assert_not_called()
            experience_validator.validate_experience.assert_called_once_with(experience)


class TestModifyExperience(object):

    def test_gets_modifies_not_none_params_and_returns_experience(self):
        experience = Experience(id='1', title='Title', description='some', author_id='2', author_username='usr')
        experience_repo = Mock()
        experience_repo.get_experience.return_value = experience

        updated_experience = Experience(id='1', title='Title', description='', author_id='2')
        experience_repo.update_experience.return_value = updated_experience

        experience_validator = Mock()
        experience_validator.validate_experience.return_value = True

        response = ModifyExperienceInteractor(experience_repo, experience_validator) \
            .set_params(id='1', title=None, description='', logged_person_id='2').execute()

        experience_repo.get_experience.assert_called_once_with(id='1')
        experience_repo.update_experience.assert_called_once_with(updated_experience)
        experience_validator.validate_experience.assert_called_once_with(updated_experience)
        assert response == updated_experience

    def test_invalid_experience_returns_error_and_doesnt_update_it(self):
        experience = Experience(id='1', title='', description='', author_id='2', author_username='usr')
        experience_repo = Mock()
        experience_repo.get_experience.return_value = experience
        experience_validator = Mock()
        experience_validator.validate_experience.side_effect = InvalidEntityException(source='s', code='c', message='m')
        updated_experience = Experience(id='1', title='Other', description='some', author_id='2')

        try:
            ModifyExperienceInteractor(experience_repo, experience_validator) \
                .set_params(id='1', title='Other', description='some', logged_person_id='2').execute()
            assert False
        except InvalidEntityException as invalid_exc:
            assert invalid_exc.source == 's'
            assert invalid_exc.code == 'c'
            assert str(invalid_exc) == 'm'
            experience_repo.get_experience.assert_called_once_with(id='1')
            experience_repo.update_experience.assert_not_called()
            experience_validator.validate_experience.assert_called_once_with(updated_experience)

    def test_unexistent_experience_returns_entity_does_not_exist_error(self):
        experience_repo = Mock()
        experience_repo.get_experience.side_effect = EntityDoesNotExistException
        experience_validator = Mock()

        try:
            ModifyExperienceInteractor(experience_repo, experience_validator) \
                .set_params(id='1', title='Other', description='some', logged_person_id='3').execute()
            assert False
        except EntityDoesNotExistException:
            pass
