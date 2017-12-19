import json

from django.conf import settings

from .repositories import PersonRepo, AuthTokenRepo, ConfirmationTokenRepo
from .validators import ClientSecretKeyValidator, PersonValidator, PersonPermissionsValidator
from .interactors import CreateGuestPersonAndReturnAuthTokenInteractor, RegisterUsernameAndEmailInteractor, \
        AuthenticateInteractor, ConfirmEmailInteractor
from .views import PeopleView, PersonView, EmailConfirmationView
from .services import MailerService


def create_person_repo():
    return PersonRepo()


def create_auth_token_repo():
    return AuthTokenRepo()


def create_confirmation_token_repo():
    return ConfirmationTokenRepo()


def create_client_secret_key_validator():
    return ClientSecretKeyValidator(valid_client_secret_key=settings.CLIENT_SECRET_KEY)


def create_person_permissions_validator():
    return PersonPermissionsValidator(person_repo=create_person_repo())


def create_person_validator():
    project_name = settings.PROJECT_NAME

    generic_forbidden_usernames_json = open('people/generic_forbidden_usernames.json')
    generic_forbidden_usernames = json.load(generic_forbidden_usernames_json)
    custom_forbidden_usernames_json = open('people/custom_forbidden_usernames.json')
    custom_forbidden_usernames = json.load(custom_forbidden_usernames_json)
    forbidden_usernames = generic_forbidden_usernames + custom_forbidden_usernames

    forbidden_email_domains_json = open('people/forbidden_email_domains.json')
    forbidden_email_domains = json.load(forbidden_email_domains_json)

    return PersonValidator(project_name=project_name, forbidden_usernames=forbidden_usernames,
                           forbidden_email_domains=forbidden_email_domains)


def create_mailer_service(request):
    return MailerService(request)


def create_authenticate_interactor():
    return AuthenticateInteractor(auth_token_repo=create_auth_token_repo())


def create_guest_person_and_return_auth_token_interactor():
    return CreateGuestPersonAndReturnAuthTokenInteractor(
            client_secret_key_validator=create_client_secret_key_validator(),
            person_repo=create_person_repo(),
            auth_token_repo=create_auth_token_repo())


def create_register_username_and_email_interactor(request):
    person_validator = create_person_validator()
    person_repo = create_person_repo()
    confirmation_token_repo = create_confirmation_token_repo()
    mailer_service = create_mailer_service(request)
    return RegisterUsernameAndEmailInteractor(person_validator=person_validator,
                                              person_repo=person_repo,
                                              confirmation_token_repo=confirmation_token_repo,
                                              mailer_service=mailer_service)


def create_confirm_email_interactor():
    return ConfirmEmailInteractor(confirmation_token_repo=create_confirmation_token_repo(),
                                  person_repo=create_person_repo())


def create_people_view(request, **kwargs):
    return PeopleView(
            create_guest_person_and_return_auth_token_interactor=create_guest_person_and_return_auth_token_interactor())


def create_person_view(request, **kwargs):
    return PersonView(register_username_and_email_interactor=create_register_username_and_email_interactor(request))


def create_email_confirmation_view(request, **kwargs):
    return EmailConfirmationView(confirm_email_interactor=create_confirm_email_interactor())
