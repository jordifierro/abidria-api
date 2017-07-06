from .factories import GetScenesFromExperienceFactory
from .serializers import MultipleScenesSerializer


class ScenesView(object):

    def get(self, experience):
        get_scenes_from_experience = GetScenesFromExperienceFactory.get()
        scenes = get_scenes_from_experience.set_params(experience_id=experience).execute()

        body = MultipleScenesSerializer.serialize(scenes)
        status = 200
        return body, status
