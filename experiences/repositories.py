from abidria.entities import Picture
from abidria.exceptions import EntityDoesNotExist
from .models import ORMExperience
from .entities import Experience


class ExperienceRepo(object):

    def _decode_db_experience(self, db_experience):
        if not db_experience.picture:
            picture = None
        else:
            picture = Picture(small_url=db_experience.picture.small.url,
                              medium_url=db_experience.picture.medium.url,
                              large_url=db_experience.picture.large.url)

        return Experience(id=db_experience.id,
                          title=db_experience.title,
                          description=db_experience.description,
                          picture=picture)

    def get_all_experiences(self):
        db_experiences = ORMExperience.objects.all()
        experiences = []
        for db_experience in db_experiences:
            experiences.append(self._decode_db_experience(db_experience))
        return experiences

    def get_experience(self, id):
        try:
            db_experience = ORMExperience.objects.get(id=id)
            return self._decode_db_experience(db_experience)
        except ORMExperience.DoesNotExist:
            raise EntityDoesNotExist()

    def create_experience(self, experience):
        db_experience = ORMExperience.objects.create(title=experience.title,
                                                     description=experience.description)
        return self._decode_db_experience(db_experience)

    def attach_picture_to_experience(self, experience_id, picture):
        experience = ORMExperience.objects.get(id=experience_id)
        experience.picture = picture
        experience.save()
        return self._decode_db_experience(experience)
