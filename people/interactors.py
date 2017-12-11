from abidria.exceptions import EntityDoesNotExistException, ConflictException
from people.entities import Person


class CreateGuestPersonAndReturnAuthTokenInteractor(object):

    def __init__(self, client_secret_key_validator, person_repo, auth_token_repo):
        self.client_secret_key_validator = client_secret_key_validator
        self.person_repo = person_repo
        self.auth_token_repo = auth_token_repo

    def set_params(self, client_secret_key):
        self.client_secret_key = client_secret_key
        return self

    def execute(self):
        self.client_secret_key_validator.validate(client_secret_key=self.client_secret_key)

        created_guest_person = self.person_repo.create_guest_person()

        return self.auth_token_repo.create_auth_token(person_id=created_guest_person.id)


class AuthenticateInteractor(object):

    def __init__(self, auth_token_repo):
        self.auth_token_repo = auth_token_repo

    def set_params(self, access_token):
        self.access_token = access_token
        return self

    def execute(self):
        try:
            auth_token = self.auth_token_repo.get_auth_token(access_token=self.access_token)
            return auth_token.person_id
        except EntityDoesNotExistException:
            return None


class RegisterUsernameAndEmailInteractor(object):

    def __init__(self, person_validator, person_repo, confirmation_token_repo, mailer_service):
        self.person_validator = person_validator
        self.person_repo = person_repo
        self.confirmation_token_repo = confirmation_token_repo
        self.mailer_service = mailer_service

    def set_params(self, logged_person_id, username, email):
        self.logged_person_id = logged_person_id
        self.username = username
        self.email = email
        return self

    def execute(self):
        person = self.person_repo.get_person(id=self.logged_person_id)
        if person.is_email_confirmed:
            raise ConflictException(source='person', code='already_registered', message='Person already registered')

        updated_person = Person(id=person.id, is_registered=True,
                                username=self.username, email=self.email, is_email_confirmed=False)
        self.person_validator.validate(updated_person)
        updated_person = self.person_repo.update_person(updated_person)

        self.confirmation_token_repo.delete_confirmation_tokens(person_id=updated_person.id)
        confirmation_token = self.confirmation_token_repo.create_confirmation_token(person_id=updated_person.id)
        self.mailer_service.send_ask_confirmation_mail(confirmation_token=confirmation_token,
                                                       username=updated_person.username, email=updated_person.email)
        return updated_person
