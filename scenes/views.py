from abidria.decorators import serialize_exceptions
from .serializers import MultipleScenesSerializer, SceneSerializer


class ScenesView(object):

    def __init__(self, get_scenes_from_experience_interactor=None, create_new_scene_interactor=None):
        self.get_scenes_from_experience_interactor = get_scenes_from_experience_interactor
        self.create_new_scene_interactor = create_new_scene_interactor

    @serialize_exceptions
    def get(self, experience):
        scenes = self.get_scenes_from_experience_interactor.set_params(experience_id=experience).execute()

        body = MultipleScenesSerializer.serialize(scenes)
        status = 200
        return body, status

    @serialize_exceptions
    def post(self, title, description, latitude, longitude, experience_id):
        scene = self.create_new_scene_interactor.set_params(title=title, description=description,
                                                            latitude=float(latitude), longitude=float(longitude),
                                                            experience_id=experience_id).execute()
        body = SceneSerializer.serialize(scene)
        status = 201
        return body, status


class SceneView(object):

    def __init__(self, modify_scene_interactor=None):
        self.modify_scene_interactor = modify_scene_interactor

    @serialize_exceptions
    def patch(self, scene_id, title=None, description=None, latitude=None, longitude=None, experience_id=None):
        latitude = float(latitude) if latitude is not None else None
        longitude = float(longitude) if longitude is not None else None

        scene = self.modify_scene_interactor.set_params(id=scene_id, title=title, description=description,
                                                        latitude=latitude, longitude=longitude,
                                                        experience_id=experience_id).execute()
        body = SceneSerializer.serialize(scene)
        status = 200
        return body, status
