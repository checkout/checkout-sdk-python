from tests.base import CheckoutSdkTestCase
from checkout_sdk.common import ResponseDTO


class ResponseDTOTests(CheckoutSdkTestCase):
    JSON = {
        "id": "pay",
        "source": {
            "id": "source",
            "type": "card",
            "billing_address": {
                "city": "London"
            }
        },
        "_links": {
            "self": {
                "href": "http://url"
            }
        },
        "dummy_array": [
            {
                "key1": "value1"
            }
        ]
    }

    def test_dto_bad_type(self):
        with self.assertRaises(TypeError):
            dto = ResponseDTO(kvp=False)

    def test_dto_immutable(self):
        dto = ResponseDTO(kvp=None, read_only=True)
        with self.assertRaises(AttributeError):
            dto.dummy = 1

    def test_dto_mutable(self):
        dto = ResponseDTO(kvp=None, read_only=False)
        dto.dummy = 1
        self.assertTrue(dto.dummy == 1)
        self.assertTrue(dto['dummy'] == dto.dummy)
        dto['dummy2'] = 1
        self.assertTrue(dto.dummy2 == 1)
        self.assertTrue(dto['dummy2'] == dto.dummy2)

    def test_dto(self):
        dto = ResponseDTO(kvp=self.JSON)
        self.assertTrue(dto.id == dto['id'])
        self.assertIsNotNone(dto.source.id)
        self.assertTrue(dto.source.id == dto['source']['id'])
        self.assertIsNotNone(dto._links)
        self.assertTrue(dto._links.self.href == dto['_links'].self['href'])
        self.assertIsNotNone(dto.dummy_array[0].key1)
        with self.assertRaises(KeyError):
            dto.key_not_found
        self.assertTrue(dto.get('key_not_found') is None)
        self.assertTrue(dto.get('key_not_found', 1) == 1)
