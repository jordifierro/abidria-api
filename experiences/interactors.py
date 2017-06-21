class GetAllExperiences(object):

    def __init__(self, experiences_repo):
        self.experiences_repo = experiences_repo

    def execute(self):
        return self.experiences_repo.get_all_experiences()


class GetExperience(object):

    def __init__(self, experience_repo, scene_repo):
        self.experience_repo = experience_repo
        self.scene_repo = scene_repo

    def set_params(self, id=None):
        self.id = id
        return self

    def execute(self):
        experience = self.experience_repo.get_experience(id=self.id)
        experience_scenes = self.scene_repo.get_scenes(experience_id=self.id)
        return experience, experience_scenes
