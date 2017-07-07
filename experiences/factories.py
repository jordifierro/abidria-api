from .repositories import ExperienceRepo
from .interactors import GetAllExperiencesInteractor


class ExperienceRepoFactory(object):

    @staticmethod
    def get():
        return ExperienceRepo()


class GetAllExperiencesInteractorFactory(object):

    @staticmethod
    def get():
        experience_repo = ExperienceRepoFactory.get()
        return GetAllExperiencesInteractor(experience_repo)


class ExperiencesViewInjector(object):

    @staticmethod
    def get_interactor():
        return GetAllExperiencesInteractorFactory.get()
