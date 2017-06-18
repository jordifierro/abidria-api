class GetAllExperiences(object):

    def __init__(self, experiences_repo):
        self.experiences_repo = experiences_repo

    def execute(self):
        return self.experiences_repo.get_all_experiences()


class GetExperience(object):

    def __init__(self, experiences_repo):
        self.experiences_repo = experiences_repo

    def set_params(self, id=None):
        self.id = id
        return self

    def execute(self):
        return self.experiences_repo.get_experience(id=self.id)
