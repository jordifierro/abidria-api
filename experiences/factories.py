from .repositories import ExperienceRepo
from .validators import ExperienceValidator
from .interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor
from .views import ExperiencesView


class ExperienceRepoFactory(object):

    @staticmethod
    def create():
        return ExperienceRepo()


class ExperienceValidatorFactory(object):

    @staticmethod
    def create():
        return ExperienceValidator()


class GetAllExperiencesInteractorFactory(object):

    @staticmethod
    def create():
        experience_repo = ExperienceRepoFactory.create()
        return GetAllExperiencesInteractor(experience_repo)


class CreateNewExperienceInteractorFactory(object):

    @staticmethod
    def create():
        experience_repo = ExperienceRepoFactory.create()
        experience_validator = ExperienceValidatorFactory.create()
        return CreateNewExperienceInteractor(experience_repo, experience_validator)


class ExperiencesViewFactory(object):

    @staticmethod
    def create():
        get_all_experiences_interactor = GetAllExperiencesInteractorFactory.create()
        create_new_experience_interactor = CreateNewExperienceInteractorFactory.create()
        return ExperiencesView(get_all_experiences_interactor=get_all_experiences_interactor,
                               create_new_experience_interactor=create_new_experience_interactor)
