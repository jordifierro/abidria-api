class PictureSerializer(object):

    @staticmethod
    def serialize(picture):
        if picture is None:
            result = None
        else:
            result = {}
            result['small'] = picture.small
            result['medium'] = picture.medium
            result['large'] = picture.large

        return result
