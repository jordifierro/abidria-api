from abidria.exceptions import EntityDoesNotExistException
from .models import ORMPerson, ORMAuthToken
from .entities import Person, AuthToken


class PersonRepo(object):

    def create_guest_person(self):
        created_orm_person = ORMPerson.objects.create()
        return self._decode_db_person(created_orm_person)

    def _decode_db_person(self, db_person):
        return Person(id=db_person.id, is_registered=db_person.is_registered,
                      username=db_person.username, email=db_person.email,
                      is_email_confirmed=db_person.is_email_confirmed)


class AuthTokenRepo(object):

    def create_auth_token(self, person_id):
        created_orm_auth_token = ORMAuthToken.objects.create(person_id=person_id)
        return self._decode_db_auth_token(created_orm_auth_token)

    def get_auth_token(self, access_token):
        try:
            orm_auth_token = ORMAuthToken.objects.get(access_token=access_token)
            return self._decode_db_auth_token(orm_auth_token)
        except ORMAuthToken.DoesNotExist:
            raise EntityDoesNotExistException

    def _decode_db_auth_token(self, db_auth_token):
        return AuthToken(person_id=db_auth_token.person_id,
                         access_token=str(db_auth_token.access_token),
                         refresh_token=str(db_auth_token.refresh_token))
