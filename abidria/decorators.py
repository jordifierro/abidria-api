from .exceptions import InvalidEntityException, EntityDoesNotExist
from .serializers import InvalidEntitySerializer, EntityDoesNotExistSerializer


def serialize_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidEntityException as e:
            body = InvalidEntitySerializer.serialize(e)
            status = 422
        except EntityDoesNotExist:
            body = EntityDoesNotExistSerializer.serialize()
            status = 404

        return body, status
    return func_wrapper
