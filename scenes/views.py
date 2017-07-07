from .serializers import MultipleScenesSerializer


class ScenesView(object):

    def __init__(self, get_scenes_from_experience_interactor):
        self.get_scenes_from_experience_interactor = get_scenes_from_experience_interactor

    def get(self, experience):
        scenes = self.get_scenes_from_experience_interactor.set_params(experience_id=experience).execute()

        body = MultipleScenesSerializer.serialize(scenes)
        status = 200
        return body, status
