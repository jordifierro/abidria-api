from .exceptions import InvalidEntityException, EntityDoesNotExistException, ConflictException, AbidriaException
from .serializers import AbidriaExceptionSerializer

exception_status_code_mapper = {
        InvalidEntityException: 422,
        EntityDoesNotExistException: 404,
        ConflictException: 409,
        }


def serialize_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AbidriaException as e:
            body = AbidriaExceptionSerializer.serialize(e)
            status = exception_status_code_mapper[type(e)]
        return body, status
    return func_wrapper
