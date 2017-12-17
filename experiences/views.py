from abidria.decorators import serialize_exceptions
from .serializers import MultipleExperiencesSerializer, ExperienceSerializer


class ExperiencesView(object):

    def __init__(self, get_all_experiences_interactor=None, create_new_experience_interactor=None):
        self.get_all_experiences_interactor = get_all_experiences_interactor
        self.create_new_experience_interactor = create_new_experience_interactor

    @serialize_exceptions
    def get(self, logged_person_id=None):
        experiences = self.get_all_experiences_interactor.set_params(logged_person_id=logged_person_id).execute()

        body = MultipleExperiencesSerializer.serialize(experiences)
        status = 200
        return body, status

    @serialize_exceptions
    def post(self, title=None, description=None, logged_person_id=None):
        experience = self.create_new_experience_interactor \
                .set_params(title=title, description=description, logged_person_id=logged_person_id).execute()
        body = ExperienceSerializer.serialize(experience)
        status = 201
        return body, status


class ExperienceView(object):

    def __init__(self, modify_experience_interactor=None):
        self.modify_experience_interactor = modify_experience_interactor

    @serialize_exceptions
    def patch(self, experience_id, title=None, description=None, logged_person_id=None):
        experience = self.modify_experience_interactor \
                .set_params(id=experience_id, title=title,
                            description=description, logged_person_id=logged_person_id).execute()
        body = ExperienceSerializer.serialize(experience)
        status = 200
        return body, status


class UploadExperiencePictureView(object):

    def __init__(self, upload_experience_picture_interactor=None):
        self.upload_experience_picture_interactor = upload_experience_picture_interactor

    @serialize_exceptions
    def post(self, experience_id, picture, logged_person_id):
        experience = self.upload_experience_picture_interactor.set_params(experience_id=experience_id, picture=picture,
                                                                          logged_person_id=logged_person_id).execute()
        body = ExperienceSerializer.serialize(experience)
        status = 200
        return body, status
