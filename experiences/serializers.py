from abidria.serializers import PictureSerializer


class MultipleExperiencesSerializer:

    @staticmethod
    def serialize(experiences):
        return [ExperienceSerializer.serialize(experience) for experience in experiences]


class ExperienceSerializer:

    @staticmethod
    def serialize(experience):
        return {
                   'id': str(experience.id),
                   'title': experience.title,
                   'description': experience.description,
                   'picture': PictureSerializer.serialize(experience.picture),
                   'author_id': experience.author_id,
                   'author_username': experience.author_username,
                   'is_mine': experience.is_mine,
                   'is_saved': experience.is_saved
               }
