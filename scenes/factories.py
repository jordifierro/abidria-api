from .repositories import SceneRepo
from .interactors import GetScenesFromExperience


class SceneRepoFactory(object):

    @staticmethod
    def get():
        return SceneRepo()


class GetScenesFromExperienceFactory(object):

    @staticmethod
    def get():
        scene_repo = SceneRepoFactory.get()
        return GetScenesFromExperience(scene_repo=scene_repo)


class ScenesViewInjector(object):

    @staticmethod
    def get_interactor():
        return GetScenesFromExperienceFactory.get()
