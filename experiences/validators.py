from abidria.exceptions import InvalidEntityException


class ExperienceValidator(object):

    MIN_TITLE_LENGHT = 1
    MAX_TITLE_LENGHT = 30

    def validate_experience(self, experience):
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
