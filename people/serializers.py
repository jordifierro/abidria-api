class AuthTokenSerializer(object):

    @staticmethod
    def serialize(auth_token):
        return {
                   'person_id': auth_token.person_id,
                   'access_token': auth_token.access_token,
                   'refresh_token': auth_token.refresh_token
               }


class PersonSerializer(object):

    @staticmethod
    def serialize(person):
        return {
                   'is_registered': person.is_registered,
                   'username': person.username,
                   'email': person.email,
                   'is_email_confirmed': person.is_email_confirmed,
               }
