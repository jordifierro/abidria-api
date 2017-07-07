from .repositories import SceneRepo
from .interactors import GetScenesFromExperienceInteractor


class SceneRepoFactory(object):

    @staticmethod
    def get():
        return SceneRepo()


class GetScenesFromExperienceInteractorFactory(object):

    @staticmethod
    def get():
        scene_repo = SceneRepoFactory.get()
        return GetScenesFromExperienceInteractor(scene_repo=scene_repo)


class ScenesViewInjector(object):

    @staticmethod
    def get_interactor():
        return GetScenesFromExperienceInteractorFactory.get()
