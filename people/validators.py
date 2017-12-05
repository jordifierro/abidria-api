from abidria.exceptions import InvalidEntityException


class ClientSecretKeyValidator(object):

    def __init__(self, valid_client_secret_key):
        self.valid_client_secret_key = valid_client_secret_key

    def validate(self, client_secret_key):
        if client_secret_key != self.valid_client_secret_key:
            raise InvalidEntityException(source='client_secret_key', code='invalid',
                                         message='Invalid client secret key')
        else:
            return True
