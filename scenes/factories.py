from experiences.factories import create_experience_repo
from .repositories import SceneRepo
from .interactors import GetScenesFromExperienceInteractor, CreateNewSceneInteractor, ModifySceneInteractor
from .validators import SceneValidator
from .views import ScenesView, SceneView


def create_scene_repo():
    return SceneRepo()


def create_scene_validator():
    return SceneValidator(create_experience_repo())


def create_get_scenes_from_experience_interactor():
    return GetScenesFromExperienceInteractor(scene_repo=create_scene_repo())


def create_create_new_scene_interactor():
    return CreateNewSceneInteractor(scene_repo=create_scene_repo(), scene_validator=create_scene_validator())


def create_modify_scene_interactor():
    return ModifySceneInteractor(scene_repo=create_scene_repo(), scene_validator=create_scene_validator())


def create_scenes_view(request, *args, **kwargs):
    return ScenesView(get_scenes_from_experience_interactor=create_get_scenes_from_experience_interactor(),
                      create_new_scene_interactor=create_create_new_scene_interactor())


def create_scene_view(request, *args, **kwargs):
    return SceneView(modify_scene_interactor=create_modify_scene_interactor())
