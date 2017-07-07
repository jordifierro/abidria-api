class GetAllExperiencesInteractor(object):

    def __init__(self, experiences_repo):
        self.experiences_repo = experiences_repo

    def execute(self):
        return self.experiences_repo.get_all_experiences()
