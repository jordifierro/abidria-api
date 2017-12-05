class AuthTokenSerializer(object):

    @staticmethod
    def serialize(auth_token):
        return {
                   'person_id': auth_token.person_id,
                   'access_token': auth_token.access_token,
                   'refresh_token': auth_token.refresh_token
               }
