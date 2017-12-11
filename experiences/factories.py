from .repositories import ExperienceRepo
from .validators import ExperienceValidator
from .interactors import GetAllExperiencesInteractor, CreateNewExperienceInteractor, \
        ModifyExperienceInteractor
from .views import ExperiencesView, ExperienceView


def create_experience_repo():
    return ExperienceRepo()


def create_experience_validator():
    return ExperienceValidator()


def create_get_all_experiences_interactor():
    return GetAllExperiencesInteractor(create_experience_repo())


def create_create_new_experience_interactor():
    return CreateNewExperienceInteractor(create_experience_repo(), create_experience_validator())


def create_modify_experience_interactor():
    return ModifyExperienceInteractor(experience_repo=create_experience_repo(),
                                      experience_validator=create_experience_validator())


def create_experiences_view(request, *args, **kwargs):
    return ExperiencesView(get_all_experiences_interactor=create_get_all_experiences_interactor(),
                           create_new_experience_interactor=create_create_new_experience_interactor())


def create_experience_view(request, *args, **kwargs):
    return ExperienceView(modify_experience_interactor=create_modify_experience_interactor())
