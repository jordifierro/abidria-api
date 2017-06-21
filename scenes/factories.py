from .repositories import SceneRepo


class SceneRepoFactory(object):

    @staticmethod
    def get():
        return SceneRepo()
