from abidria.exceptions import InvalidEntityException, EntityDoesNotExistException
from abidria.decorators import serialize_exceptions


class TestSerializeExpceptionsDecorator:

    def test_invalid_entity_expceptions_returns_serialized_and_422(self):
        def raiser_func():
            raise InvalidEntityException('title', 'empty_attribute', 'Title must not be empty')

        body, status = serialize_exceptions(raiser_func)()

        assert status == 422
        assert body == {
                           'error': {
                                        'source': 'title',
                                        'code': 'empty_attribute',
                                        'message': 'Title must not be empty',
                                    }
                       }

    def test_entity_does_not_exist_exceptions_returns_serialized_and_404(self):
        def raiser_func():
            raise EntityDoesNotExistException()

        body, status = serialize_exceptions(raiser_func)()

        assert status == 404
        assert body == {
                           'error': {
                                        'source': 'entity',
                                        'code': 'not_found',
                                        'message': 'Entity not found',
                                    }
                       }
