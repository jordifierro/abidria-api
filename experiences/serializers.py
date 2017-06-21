from abidria.serializers import PictureSerializer
from scenes.serializers import MultipleScenesSerializer


class MultipleExperiencesSerializer(object):

    @staticmethod
    def serialize(experiences):
        result = []

        for experience in experiences:
            result.append(ExperienceSerializer.serialize(experience))

        return result


class ExperienceWithScenesSerializer(object):

    @staticmethod
    def serialize(experience, scenes):
        result = ExperienceSerializer.serialize(experience)
        result['scenes'] = MultipleScenesSerializer.serialize(scenes)

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
