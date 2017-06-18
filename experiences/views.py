from .factories import GetAllExperiencesFactory
from .serializers import MultipleExperiencesSerializer


class ExperiencesView(object):

    def get(self):
        get_all_experiences = GetAllExperiencesFactory.get()
        experiences = get_all_experiences.execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status
