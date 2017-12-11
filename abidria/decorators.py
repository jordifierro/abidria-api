from .exceptions import InvalidEntityException, EntityDoesNotExistException, ConflictException
from .serializers import InvalidEntitySerializer, EntityDoesNotExistSerializer, ConflictExceptionSerializer


def serialize_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidEntityException as e:
            body = InvalidEntitySerializer.serialize(e)
            status = 422
        except EntityDoesNotExistException:
            body = EntityDoesNotExistSerializer.serialize()
            status = 404
        except ConflictException as e:
            body = ConflictExceptionSerializer.serialize(e)
            status = 409

        return body, status
    return func_wrapper
