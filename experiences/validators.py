from abidria.exceptions import InvalidEntityException, NoPermissionException


class ExperienceValidator(object):

    MIN_TITLE_LENGHT = 1
    MAX_TITLE_LENGHT = 30

    def validate_experience(self, experience):
        if experience.author_id is None:
            raise InvalidEntityException(source='author', code='empty_attribute', message='Author cannot be empty')
        if experience.title is None:
            raise InvalidEntityException(source='title', code='empty_attribute', message='Title cannot be empty')
        if type(experience.title) is not str:
            raise InvalidEntityException(source='title', code='wrong_type', message='Title must be string')
        if len(experience.title) < ExperienceValidator.MIN_TITLE_LENGHT or \
           len(experience.title) > ExperienceValidator.MAX_TITLE_LENGHT:
            raise InvalidEntityException(source='title', code='wrong_size',
                                         message='Title must be between 1 and 30 chars')

        if experience.description is not None and type(experience.description) is not str:
            raise InvalidEntityException(source='description', code='wrong_type', message='Description must be string')

        return True


class ExperiencePermissionsValidator(object):

    def __init__(self, experience_repo, person_permissions_validator):
        self.experience_repo = experience_repo
        self.person_permissions_validator = person_permissions_validator

    def validate_permissions(self, logged_person_id, has_permissions_to_modify_experience=None):
        self.person_permissions_validator.validate_permissions(logged_person_id=logged_person_id)

        if has_permissions_to_modify_experience is not None:
            experience = self.experience_repo.get_experience(id=has_permissions_to_modify_experience)
            if experience.author_id != logged_person_id:
                raise NoPermissionException()

        return True
