class PictureSerializer:

    @staticmethod
    def serialize(picture):
        if picture is None:
            return None

        return {
                   'small_url': picture.small_url,
                   'medium_url': picture.medium_url,
                   'large_url': picture.large_url,
               }


class AbidriaExceptionSerializer:

    @staticmethod
    def serialize(exception):
        return {
                   'error': {
                       'source': exception.source,
                       'code': exception.code,
                       'message': str(exception)
                    }
               }
