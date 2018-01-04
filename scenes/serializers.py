from abidria.serializers import PictureSerializer


class MultipleScenesSerializer:

    @staticmethod
    def serialize(scenes):
        return [SceneSerializer.serialize(scene) for scene in scenes]


class SceneSerializer:

    @staticmethod
    def serialize(scene):
        return {
                   'id': str(scene.id),
                   'title': scene.title,
                   'description': scene.description,
                   'picture': PictureSerializer.serialize(scene.picture),
                   'latitude': float(scene.latitude),
                   'longitude': float(scene.longitude),
                   'experience_id': str(scene.experience_id),
               }
