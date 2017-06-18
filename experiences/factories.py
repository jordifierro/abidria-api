from .models import ORMExperience
from .repositories import ExperienceRepo
from .interactors import GetAllExperiences


class ExperienceRepoFactory(object):

    @staticmethod
    def get():
        experiences_objects = ORMExperience.objects
        return ExperienceRepo(experiences_objects)


class GetAllExperiencesFactory(object):

    @staticmethod
    def get():
        experience_repo = ExperienceRepoFactory.get()
        return GetAllExperiences(experience_repo)
