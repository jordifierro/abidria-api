class PictureSerializer(object):

    @staticmethod
    def serialize(picture):
        if picture is None:
            return None

        return {
                   'small': picture.small,
                   'medium': picture.medium,
                   'large': picture.large,
               }
