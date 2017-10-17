from .entities import Scene


class GetScenesFromExperienceInteractor(object):

    def __init__(self, scene_repo):
        self.scene_repo = scene_repo

    def set_params(self, experience_id):
        self.experience_id = experience_id
        return self

    def execute(self):
        return self.scene_repo.get_scenes(experience_id=self.experience_id)


class CreateNewSceneInteractor(object):

    def __init__(self, scene_repo, scene_validator):
        self.scene_repo = scene_repo
        self.scene_validator = scene_validator

    def set_params(self, title, description, latitude, longitude, experience_id):
        self.title = title
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.experience_id = experience_id
        return self

    def execute(self):
        scene = Scene(title=self.title, description=self.description,
                      latitude=self.latitude, longitude=self.longitude, experience_id=self.experience_id)
        self.scene_validator.validate_scene(scene)
        return self.scene_repo.save_scene(scene)
