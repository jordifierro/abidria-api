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
