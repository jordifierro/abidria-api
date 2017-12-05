from abidria.decorators import serialize_exceptions
from .serializers import AuthTokenSerializer


class PeopleView(object):

    def __init__(self, create_guest_person_and_return_auth_token_interactor=None):
        self.create_guest_person_and_return_auth_token_interactor = create_guest_person_and_return_auth_token_interactor

    @serialize_exceptions
    def post(self, client_secret_key):
        auth_token = self.create_guest_person_and_return_auth_token_interactor \
                .set_params(client_secret_key=client_secret_key).execute()

        body = AuthTokenSerializer.serialize(auth_token)
        status = 201
        return body, status
