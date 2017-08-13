from .repositories import SceneRepo
from .interactors import GetScenesFromExperienceInteractor
from .views import ScenesView


class SceneRepoFactory(object):

    @staticmethod
    def create():
        return SceneRepo()


class GetScenesFromExperienceInteractorFactory(object):

    @staticmethod
    def create():
        scene_repo = SceneRepoFactory.create()
        return GetScenesFromExperienceInteractor(scene_repo=scene_repo)


class ScenesViewFactory(object):

    @staticmethod
    def create():
        get_scenes_from_experience_interactor = GetScenesFromExperienceInteractorFactory.create()
        return ScenesView(get_scenes_from_experience_interactor)
