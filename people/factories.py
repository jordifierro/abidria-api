from django.conf import settings

from .repositories import PersonRepo, AuthTokenRepo
from .validators import ClientSecretKeyValidator
from .interactors import CreateGuestPersonAndReturnAuthTokenInteractor
from .views import PeopleView


def create_person_repo():
    return PersonRepo()


def create_auth_token_repo():
    return AuthTokenRepo()


def create_client_secret_key_validator():
    return ClientSecretKeyValidator(valid_client_secret_key=settings.CLIENT_SECRET_KEY)


def create_guest_person_and_return_auth_token_interactor():
    return CreateGuestPersonAndReturnAuthTokenInteractor(
            client_secret_key_validator=create_client_secret_key_validator(),
            person_repo=create_person_repo(),
            auth_token_repo=create_auth_token_repo())


def create_people_view():
    return PeopleView(
            create_guest_person_and_return_auth_token_interactor=create_guest_person_and_return_auth_token_interactor())
