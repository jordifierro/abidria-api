from .serializers import MultipleExperiencesSerializer


class ExperiencesView(object):

    def __init__(self, get_all_experiences_interactor):
        self.get_all_experiences_interactor = get_all_experiences_interactor

    def get(self):
        experiences = self.get_all_experiences_interactor.execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status
