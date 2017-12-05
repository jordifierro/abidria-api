from abidria.exceptions import InvalidEntityException
from people.validators import ClientSecretKeyValidator


class TestClientSecretKeyValidator(object):

    def test_valid_key(self):
        TestClientSecretKeyValidator._ScenarioMaker() \
                .given_a_client_secret_key_validator_with_valid_key('A') \
                .when_key_is_validated('A') \
                .then_response_should_be_true()

    def test_invalid_key(self):
        TestClientSecretKeyValidator._ScenarioMaker() \
                .given_a_client_secret_key_validator_with_valid_key('A') \
                .when_key_is_validated('B') \
                .then_should_raise_invalid_entity_execption()

    class _ScenarioMaker(object):

        def __init__(self):
            self.validator = None
            self.response = None
            self.error = None

        def given_a_client_secret_key_validator_with_valid_key(self, key):
            self.validator = ClientSecretKeyValidator(valid_client_secret_key=key)
            return self

        def when_key_is_validated(self, key):
            try:
                self.response = self.validator.validate(client_secret_key=key)
            except InvalidEntityException as e:
                self.error = e
            return self

        def then_response_should_be_true(self):
            assert self.response is True
            return self

        def then_should_raise_invalid_entity_execption(self):
            assert self.error.source == 'client_secret_key'
            assert self.error.code == 'invalid'
            assert str(self.error) == 'Invalid client secret key'
            return self
