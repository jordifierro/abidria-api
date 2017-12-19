from experiences.factories import create_experience_repo, create_experience_permissions_validator
from .repositories import SceneRepo
from .interactors import GetScenesFromExperienceInteractor, CreateNewSceneInteractor, ModifySceneInteractor, \
        UploadScenePictureInteractor
from .validators import SceneValidator, ScenePermissionsValidator
from .views import ScenesView, SceneView, UploadScenePictureView


def create_scene_repo():
    return SceneRepo()


def create_scene_validator():
    return SceneValidator(create_experience_repo())


def create_scene_permissions_validator():
    return ScenePermissionsValidator(scene_repo=create_scene_repo(),
                                     experience_permissions_validator=create_experience_permissions_validator())


def create_get_scenes_from_experience_interactor():
    return GetScenesFromExperienceInteractor(scene_repo=create_scene_repo(),
                                             permissions_validator=create_experience_permissions_validator())


def create_create_new_scene_interactor():
    return CreateNewSceneInteractor(scene_repo=create_scene_repo(), scene_validator=create_scene_validator(),
                                    permissions_validator=create_experience_permissions_validator())


def create_modify_scene_interactor():
    return ModifySceneInteractor(scene_repo=create_scene_repo(), scene_validator=create_scene_validator(),
                                 permissions_validator=create_experience_permissions_validator())


def create_upload_scene_picture_interactor():
    return UploadScenePictureInteractor(scene_repo=create_scene_repo(),
                                        permissions_validator=create_scene_permissions_validator())


def create_scenes_view(request, **kwargs):
    return ScenesView(get_scenes_from_experience_interactor=create_get_scenes_from_experience_interactor(),
                      create_new_scene_interactor=create_create_new_scene_interactor())


def create_scene_view(request, **kwargs):
    return SceneView(modify_scene_interactor=create_modify_scene_interactor())


def create_upload_scene_picture_view(request, **kwargs):
    return UploadScenePictureView(upload_scene_picture_interactor=create_upload_scene_picture_interactor())
