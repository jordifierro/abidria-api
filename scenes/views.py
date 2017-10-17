from abidria.serializers import InvalidEntitySerializer
from abidria.exceptions import InvalidEntityException
from .serializers import MultipleScenesSerializer, SceneSerializer


class ScenesView(object):

    def __init__(self, get_scenes_from_experience_interactor=None, create_new_scene_interactor=None):
        self.get_scenes_from_experience_interactor = get_scenes_from_experience_interactor
        self.create_new_scene_interactor = create_new_scene_interactor

    def get(self, experience):
        scenes = self.get_scenes_from_experience_interactor.set_params(experience_id=experience).execute()

        body = MultipleScenesSerializer.serialize(scenes)
        status = 200
        return body, status

    def post(self, title, description, latitude, longitude, experience_id):
        try:
            scene = self.create_new_scene_interactor.set_params(title=title, description=description,
                                                                latitude=float(latitude), longitude=float(longitude),
                                                                experience_id=experience_id).execute()
            body = SceneSerializer.serialize(scene)
            status = 200
        except InvalidEntityException as e:
            body = InvalidEntitySerializer.serialize(e)
            status = 422

        return body, status
