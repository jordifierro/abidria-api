from experiences.entities import Experience


class GetAllExperiencesInteractor(object):

    def __init__(self, experiences_repo):
        self.experiences_repo = experiences_repo

    def execute(self):
        return self.experiences_repo.get_all_experiences()


class CreateNewExperienceInteractor(object):

    def __init__(self, experience_repo, experience_validator):
        self.experience_repo = experience_repo
        self.experience_validator = experience_validator

    def set_params(self, title, description):
        self.title = title
        self.description = description
        return self

    def execute(self):
        experience = Experience(title=self.title, description=self.description)
        self.experience_validator.validate_experience(experience)
        return self.experience_repo.create_experience(experience)
