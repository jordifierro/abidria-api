class Person(object):

    def __init__(self, id=None, is_registered=False, username=None, email=None, is_email_confirmed=None):
        self._id = id
        self._is_registered = is_registered
        self._username = username
        self._email = email
        self._is_email_confirmed = is_email_confirmed

    @property
    def id(self):
        return self._id

    @property
    def is_registered(self):
        return self._is_registered

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def is_email_confirmed(self):
        return self._is_email_confirmed

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class AuthToken(object):

    def __init__(self, person_id, access_token, refresh_token):
        self._person_id = person_id
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def person_id(self):
        return self._person_id

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
