class PictureSerializer(object):

    @staticmethod
    def serialize(picture):
        if picture is None:
            return None

        return {
                   'small_url': picture.small_url,
                   'medium_url': picture.medium_url,
                   'large_url': picture.large_url,
               }


class InvalidEntitySerializer(object):

    @staticmethod
    def serialize(exception):
        return {
                   'error': {
                       'source': exception.source,
                       'code': exception.code,
                       'message': str(exception)
                    }
               }


class EntityDoesNotExistSerializer(object):

    @staticmethod
    def serialize():
        return {
                   'error': {
                       'source': 'entity',
                       'code': 'not_found',
                       'message': 'Entity not found',
                    }
               }


class ConflictExceptionSerializer(object):

    @staticmethod
    def serialize(exception):
        return {
                   'error': {
                       'source': exception.source,
                       'code': exception.code,
                       'message': str(exception)
                    }
               }
