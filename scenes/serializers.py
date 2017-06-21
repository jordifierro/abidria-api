from abidria.serializers import PictureSerializer


class MultipleScenesSerializer(object):

    @staticmethod
    def serialize(scenes):
        result = []

        for scene in scenes:
            result.append(SceneSerializer.serialize(scene))

        return result


class SceneSerializer(object):

    @staticmethod
    def serialize(scene):
        result = {}

        result['id'] = scene.id
        result['title'] = scene.title
        result['description'] = scene.description
        result['picture'] = PictureSerializer.serialize(scene.picture)
        result['latitude'] = float(scene.latitude)
        result['longitude'] = float(scene.longitude)
        result['experience_id'] = scene.experience_id

        return result
