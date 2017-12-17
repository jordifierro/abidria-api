import re

from abidria.exceptions import InvalidEntityException, NoLoggedException, NoPermissionException


class ClientSecretKeyValidator(object):

    def __init__(self, valid_client_secret_key):
        self.valid_client_secret_key = valid_client_secret_key

    def validate(self, client_secret_key):
        if client_secret_key != self.valid_client_secret_key:
            raise InvalidEntityException(source='client_secret_key', code='invalid',
                                         message='Invalid client secret key')
        else:
            return True


class PersonValidator(object):

    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 20
    USERNAME_REGEX = '(?!\.)(?!\_)(?!.*?\.\.)(?!.*?\.\_)(?!.*?\_\.)(?!.*?\_\_)(?!.*\.$)(?!.*\_$)[a-z0-9_.]+$'

    def __init__(self, project_name, forbidden_usernames, forbidden_email_domains):
        self.project_name = project_name
        self.forbidden_usernames = forbidden_usernames
        self.forbidden_email_domains = forbidden_email_domains

    def validate(self, person):
        if len(person.username) < PersonValidator.USERNAME_MIN_LENGTH or \
                len(person.username) > PersonValidator.USERNAME_MAX_LENGTH:
            raise InvalidEntityException(source='username', code='wrong_size',
                                         message='Username length should be between 1 and 20 chars')
        if not re.match(PersonValidator.USERNAME_REGEX, person.username):
            raise InvalidEntityException(source='username', code='not_allowed', message='Username not allowed')
        if self.project_name in person.username:
            raise InvalidEntityException(source='username', code='not_allowed', message='Username not allowed')
        if person.username in self.forbidden_usernames:
            raise InvalidEntityException(source='username', code='not_allowed', message='Username not allowed')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", person.email):
            raise InvalidEntityException(source='email', code='wrong', message='Email is wrong')
        if person.email.split('@')[-1] in self.forbidden_email_domains:
            raise InvalidEntityException(source='email', code='not_allowed', message='Email not allowed')

        return True


class PersonPermissionsValidator(object):

    def __init__(self, person_repo):
        self.person_repo = person_repo

    def validate_permissions(self, logged_person_id, wants_to_create_content=False):
        if logged_person_id is None:
            raise NoLoggedException()

        if wants_to_create_content:
            if not self.person_repo.get_person(id=logged_person_id).is_email_confirmed:
                raise NoPermissionException()

        return True
