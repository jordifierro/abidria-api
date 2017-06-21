from decimal import Decimal

from django.test import TestCase

from experiences.models import ORMExperience
from scenes.models import ORMScene
from scenes.repositories import SceneRepo
from scenes.entities import Scene


class ExperienceRepoTestCase(TestCase):

    def test_get_all_scenes_of_an_experience(self):
        orm_exp = ORMExperience.objects.create(title='Exp a', description='some description')
        orm_sce_1 = ORMScene.objects.create(title='S1', description='desc 1', latitude=Decimal('1.2'),
                                            longitude=Decimal('-3.4'), experience=orm_exp)
        orm_sce_2 = ORMScene.objects.create(title='S2', description='desc 2', latitude=Decimal('5.6'),
                                            longitude=Decimal('-7.8'), experience=orm_exp)
        ORMScene.objects.create(title='other', description='not belongs to experience',
                                latitude=Decimal('5.6'), longitude=Decimal('-7.8'))

        result = SceneRepo().get_scenes(experience_id=orm_exp.id)

        scene_1 = Scene(id=orm_sce_1.id, title='S1', description='desc 1', picture=None,
                        latitude=Decimal('1.2'), longitude=Decimal('-3.4'), experience_id=orm_exp.id)
        scene_2 = Scene(id=orm_sce_2.id, title='S2', description='desc 2', picture=None,
                        latitude=Decimal('5.6'), longitude=Decimal('-7.8'), experience_id=orm_exp.id)
        assert result == [scene_1, scene_2] or result == [scene_2, scene_1]
