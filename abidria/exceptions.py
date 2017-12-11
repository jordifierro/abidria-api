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


class EntityDoesNotExistException(Exception):

    @property
    def source(self):
        return 'entity'

    @property
    def code(self):
        return 'not_found'

    def __str__(self):
        return 'Entity not found'


class ConflictException(Exception):

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
