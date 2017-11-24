from abidria.exceptions import InvalidEntityException
from abidria.serializers import InvalidEntitySerializer
from .serializers import MultipleExperiencesSerializer, ExperienceSerializer


class ExperiencesView(object):

    def __init__(self, get_all_experiences_interactor=None, create_new_experience_interactor=None):
        self.get_all_experiences_interactor = get_all_experiences_interactor
        self.create_new_experience_interactor = create_new_experience_interactor

    def get(self):
        experiences = self.get_all_experiences_interactor.execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status

    def post(self, title=None, description=None):
        try:
            experience = self.create_new_experience_interactor \
                    .set_params(title=title, description=description).execute()
            body = ExperienceSerializer.serialize(experience)
            status = 201
        except InvalidEntityException as e:
            body = InvalidEntitySerializer.serialize(e)
            status = 422

        return body, status
