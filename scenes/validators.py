from abidria.exceptions import InvalidEntityException, EntityDoesNotExist


class SceneValidator(object):

    MIN_TITLE_LENGHT = 1
    MAX_TITLE_LENGHT = 30
    MIN_LATITUDE = -90
    MAX_LATITUDE = +90
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = +180

    def __init__(self, experience_repo):
        self.experience_repo = experience_repo

    def validate_scene(self, scene):
        if scene.title is None:
            raise InvalidEntityException(source='title', code='empty_attribute', message='Title cannot be empty')
        if type(scene.title) is not str:
            raise InvalidEntityException(source='title', code='wrong_type', message='Title must be string')
        if len(scene.title) < SceneValidator.MIN_TITLE_LENGHT or len(scene.title) > SceneValidator.MAX_TITLE_LENGHT:
            raise InvalidEntityException(source='title', code='wrong_size',
                                         message='Title must be between 1 and 30 chars')

        if scene.description is not None and type(scene.description) is not str:
            raise InvalidEntityException(source='description', code='wrong_type', message='Description must be string')

        if scene.latitude is None:
            raise InvalidEntityException(source='latitude', code='empty_attribute', message='Latitude cannot be empty')
        if not isinstance(scene.latitude, (int, float, complex)):
            raise InvalidEntityException(source='latitude', code='wrong_type', message='Latitude must be numeric')
        if scene.latitude < SceneValidator.MIN_LATITUDE or scene.latitude > SceneValidator.MAX_LATITUDE:
            raise InvalidEntityException(source='latitude', code='wrong_size',
                                         message='Latitude must be between -90 and +90')

        if scene.longitude is None:
            raise InvalidEntityException(source='longitude', code='empty_attribute',
                                         message='Longitude cannot be empty')
        if not isinstance(scene.longitude, (int, float, complex)):
            raise InvalidEntityException(source='longitude', code='wrong_type', message='Longitude must be numeric')
        if scene.longitude < SceneValidator.MIN_LONGITUDE or scene.longitude > SceneValidator.MAX_LONGITUDE:
            raise InvalidEntityException(source='longitude', code='wrong_size',
                                         message='Longitude must be between -180 and +180')

        if scene.experience_id is None:
            raise InvalidEntityException(source='experience_id', code='empty_attribute',
                                         message='Experience id cannot be empty')
        try:
            self.experience_repo.get_experience(scene.experience_id)
        except EntityDoesNotExist:
            raise InvalidEntityException(source='experience_id', code='does_not_exist',
                                         message='Experience does not exist')

        return True
