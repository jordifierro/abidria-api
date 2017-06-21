from scenes.factories import SceneRepoFactory
from .repositories import ExperienceRepo
from .interactors import GetAllExperiences, GetExperience


class ExperienceRepoFactory(object):

    @staticmethod
    def get():
        return ExperienceRepo()


class GetAllExperiencesFactory(object):

    @staticmethod
    def get():
        experience_repo = ExperienceRepoFactory.get()
        return GetAllExperiences(experience_repo)


class GetExperienceFactory(object):

    @staticmethod
    def get():
        experience_repo = ExperienceRepoFactory.get()
        scene_repo = SceneRepoFactory.get()
        return GetExperience(experience_repo, scene_repo)
