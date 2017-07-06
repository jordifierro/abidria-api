from .repositories import ExperienceRepo
from .interactors import GetAllExperiences


class ExperienceRepoFactory(object):

    @staticmethod
    def get():
        return ExperienceRepo()


class GetAllExperiencesFactory(object):

    @staticmethod
    def get():
        experience_repo = ExperienceRepoFactory.get()
        return GetAllExperiences(experience_repo)
