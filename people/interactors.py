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
