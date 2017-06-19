from abidria.serializers import PictureSerializer


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
