class GetScenesFromExperience(object):

    def __init__(self, scene_repo):
        self.scene_repo = scene_repo

    def set_params(self, experience_id):
        self.experience_id = experience_id
        return self

    def execute(self):
        return self.scene_repo.get_scenes(experience_id=self.experience_id)
