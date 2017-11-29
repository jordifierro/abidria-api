class EntityDoesNotExistException(Exception):
    pass


class InvalidEntityException(Exception):

    def __init__(self, source, code, message):
        super().__init__(message)
        self._source = source
        self._code = code

    @property
    def source(self):
        return self._source

    @property
    def code(self):
        return self._code
