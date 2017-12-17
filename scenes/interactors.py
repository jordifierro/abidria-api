from .entities import Scene


class GetScenesFromExperienceInteractor(object):

    def __init__(self, scene_repo, permissions_validator):
        self.scene_repo = scene_repo
        self.permissions_validator = permissions_validator

    def set_params(self, experience_id, logged_person_id):
        self.experience_id = experience_id
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id)
        return self.scene_repo.get_scenes(experience_id=self.experience_id)


class CreateNewSceneInteractor(object):

    def __init__(self, scene_repo, scene_validator, permissions_validator):
        self.scene_repo = scene_repo
        self.scene_validator = scene_validator
        self.permissions_validator = permissions_validator

    def set_params(self, title, description, latitude, longitude, experience_id, logged_person_id):
        self.title = title
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.experience_id = experience_id
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id,
                                                        has_permissions_to_modify_experience=self.experience_id)
        scene = Scene(title=self.title, description=self.description,
                      latitude=self.latitude, longitude=self.longitude, experience_id=self.experience_id)
        self.scene_validator.validate_scene(scene)
        return self.scene_repo.create_scene(scene)


class ModifySceneInteractor(object):

    def __init__(self, scene_repo, scene_validator, permissions_validator):
        self.scene_repo = scene_repo
        self.scene_validator = scene_validator
        self.permissions_validator = permissions_validator

    def set_params(self, id, title, description, latitude, longitude, experience_id, logged_person_id):
        self.id = id
        self.title = title
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.experience_id = experience_id
        self.logged_person_id = logged_person_id
        return self

    def execute(self):
        self.permissions_validator.validate_permissions(logged_person_id=self.logged_person_id,
                                                        has_permissions_to_modify_experience=self.experience_id)

        scene = self.scene_repo.get_scene(id=self.id)

        new_title = self.title if self.title is not None else scene.title
        new_description = self.description if self.description is not None else scene.description
        new_latitude = self.latitude if self.latitude is not None else scene.latitude
        new_longitude = self.longitude if self.longitude is not None else scene.longitude
        new_experience_id = self.experience_id if self.experience_id is not None else scene.experience_id
        updated_scene = Scene(id=scene.id, title=new_title, description=new_description, latitude=new_latitude,
                              longitude=new_longitude, experience_id=new_experience_id)

        self.scene_validator.validate_scene(updated_scene)

        return self.scene_repo.update_scene(updated_scene)
