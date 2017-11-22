from abidria.entities import Picture
from abidria.exceptions import EntityDoesNotExist
from .models import ORMScene
from .entities import Scene


class SceneRepo(object):

    def get_scenes(self, experience_id):
        db_scenes = ORMScene.objects.filter(experience_id=experience_id)
        scenes = []
        for db_scene in db_scenes:
            scenes.append(self._decode_db_scene(db_scene))
        return scenes

    def get_scene(self, id):
        try:
            orm_scene = ORMScene.objects.get(id=id)
        except ORMScene.DoesNotExist:
            raise EntityDoesNotExist

        return self._decode_db_scene(orm_scene)

    def create_scene(self, scene):
        created_orm_scene = ORMScene.objects.create(title=scene.title,
                                                    description=scene.description,
                                                    latitude=scene.latitude,
                                                    longitude=scene.longitude,
                                                    experience_id=scene.experience_id)
        return self._decode_db_scene(created_orm_scene)

    def update_scene(self, scene):
        orm_scene = ORMScene.objects.get(id=scene.id)

        orm_scene.title = scene.title
        orm_scene.description = scene.description
        orm_scene.latitude = scene.latitude
        orm_scene.longitude = scene.longitude
        orm_scene.experience_id = scene.experience_id

        orm_scene.save()
        return self._decode_db_scene(orm_scene)

    def attach_picture_to_scene(self, scene_id, picture):
        scene = ORMScene.objects.get(id=scene_id)
        scene.picture = picture
        scene.save()
        return self._decode_db_scene(scene)

    def _decode_db_scene(self, db_scene):
        if not db_scene.picture:
            picture = None
        else:
            picture = Picture(small_url=db_scene.picture.small.url,
                              medium_url=db_scene.picture.medium.url,
                              large_url=db_scene.picture.large.url)

        return Scene(id=db_scene.id,
                     title=db_scene.title,
                     description=db_scene.description,
                     picture=picture,
                     latitude=db_scene.latitude,
                     longitude=db_scene.longitude,
                     experience_id=db_scene.experience_id)
