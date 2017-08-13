from .repositories import ExperienceRepo
from .interactors import GetAllExperiencesInteractor
from .views import ExperiencesView


class ExperienceRepoFactory(object):

    @staticmethod
    def create():
        return ExperienceRepo()


class GetAllExperiencesInteractorFactory(object):

    @staticmethod
    def create():
        experience_repo = ExperienceRepoFactory.create()
        return GetAllExperiencesInteractor(experience_repo)


class ExperiencesViewFactory(object):

    @staticmethod
    def create():
        get_all_experiences_interactor = GetAllExperiencesInteractorFactory.create()
        return ExperiencesView(get_all_experiences_interactor)
