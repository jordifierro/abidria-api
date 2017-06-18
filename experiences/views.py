from .factories import GetAllExperiencesFactory, GetExperienceFactory
from .serializers import MultipleExperiencesSerializer, ExperienceSerializer


class ExperiencesView(object):

    def get(self):
        get_all_experiences = GetAllExperiencesFactory.get()
        experiences = get_all_experiences.execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status


class ExperienceDetailView(object):

    def get(self, id=None):
        get_experience = GetExperienceFactory.get()
        experience = get_experience.set_params(id=int(id)).execute()

        body = ExperienceSerializer.serialize(experience)
        status = 200
        return body, status
