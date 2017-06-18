class MultipleExperiencesSerializer(object):

    @staticmethod
    def serialize(experiences):
        result = []

        for experience in experiences:
            result.append(ExperienceSerializer.serialize(experience))

        return result


class ExperienceSerializer(object):

    @staticmethod
    def serialize(experience):
        result = {}

        result['id'] = experience.id
        result['title'] = experience.title
        result['description'] = experience.description
        result['picture'] = PictureSerializer.serialize(experience.picture)

        return result


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
