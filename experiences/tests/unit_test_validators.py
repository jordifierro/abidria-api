from mock import Mock

from abidria.exceptions import InvalidEntityException
from experiences.validators import ExperienceValidator
from experiences.entities import Experience


class TestExperienceValidator(object):

    def test_valid_experience_returns_true(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience() \
                .when_experience_is_validated() \
                .then_response_should_be_true()

    def test_no_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title=None) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='empty_attribute',
                                             message='Title cannot be empty')

    def test_wrong_type_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title=1) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_type',
                                             message='Title must be string')

    def test_void_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title='') \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_size',
                                             message='Title must be between 1 and 30 chars')

    def test_large_title_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(title='*'*31) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='title', code='wrong_size',
                                             message='Title must be between 1 and 30 chars')

    def test_wrong_type_description_experience_returns_error(self):
        TestExperienceValidator._ScenarioMaker() \
                .given_an_experience(description=1) \
                .when_experience_is_validated() \
                .then_error_should_be_raised(source='description', code='wrong_type',
                                             message='Description must be string')

    class _ScenarioMaker(object):

        def __init__(self):
            self._experience_repo = Mock()
            self._experience_repo.get_experience.return_value = True
            self._experience = None
            self._response = None
            self._error = None

        def given_an_experience(self, title='Valid Title', description=None):
            self._experience = Experience(title=title, description=description)
            return self

        def when_experience_is_validated(self):
            validator = ExperienceValidator()
            try:
                self._response = validator.validate_experience(self._experience)
            except InvalidEntityException as e:
                self._error = e
            return self

        def then_response_should_be_true(self):
            assert self._response is True
            return self

        def then_error_should_be_raised(self, source=None, code=None, message=None):
            assert self._error.source == source
            assert self._error.code == code
            assert str(self._error) == message
            return self
