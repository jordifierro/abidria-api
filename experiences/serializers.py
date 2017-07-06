from abidria.serializers import PictureSerializer
from scenes.serializers import MultipleScenesSerializer


class MultipleExperiencesSerializer(object):

    @staticmethod
    def serialize(experiences):
        return [ExperienceSerializer.serialize(experience) for experience in experiences]


class ExperienceWithScenesSerializer(object):

    @staticmethod
    def serialize(experience, scenes):
        result = ExperienceSerializer.serialize(experience)
        result['scenes'] = MultipleScenesSerializer.serialize(scenes)

        return result


class ExperienceSerializer(object):

    @staticmethod
    def serialize(experience):
        return {
                   'id': str(experience.id),
                   'title': experience.title,
                   'description': experience.description,
                   'picture': PictureSerializer.serialize(experience.picture),
               }
