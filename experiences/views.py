from .factories import GetAllExperiencesFactory, GetExperienceFactory
from .serializers import MultipleExperiencesSerializer, ExperienceWithScenesSerializer


class ExperiencesView(object):

    def get(self):
        get_all_experiences = GetAllExperiencesFactory.get()
        experiences = get_all_experiences.execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status


class ExperienceDetailView(object):

    def get(self, id):
        get_experience = GetExperienceFactory.get()
        experience, experience_scenes = get_experience.set_params(id=int(id)).execute()

        body = ExperienceWithScenesSerializer.serialize(experience, experience_scenes)
        status = 200
        return body, status
