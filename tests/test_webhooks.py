from unittest import mock

from checkout_sdk.common import Event
from checkout_sdk.errors import InvalidSignatureError
from checkout_sdk.webhooks import parse
from checkout_sdk.webhooks.utils import _to_bytes, _to_string, verify_signature
from tests.base import CheckoutSdkTestCase


class WebhooksTests(CheckoutSdkTestCase):
    EVENT_REQUEST_BODY = {
        "eventType": "charge.refunded",
        "message": {
            "id": "charge_test_E018DBAE674I64D9AEE9",
            "originalId": "charge_test_C5C8EBAE674W64D9AED3",
            "liveMode": False,
            "created": "2016-05-20T06:02:18Z",
            "value": 2000,
            "currency": "USD",
            "trackId": "TRK1234",
            "description": "Description",
            "chargeMode": 1,
            "responseMessage": "Approved",
            "responseAdvancedInfo": "Approved",
            "responseCode": "10000",
            "status": "Refunded",
            "hasChargeback": "N",
            "metadata": {
                "trackid": "10055"
            },
            "products": [{
                "name": "T-Shirt Ladies",
                "description": "T-Shirt Ladies Medium",
                "sku": "tee123",
                "price": 2000,
                "quantity": 1,
                "image": "http://www.example.com/tshirt.jpg",
                "shippingCost": 0,
                "trackingUrl": "http://www.example.com"
            }, {
                "name": "Watch Ladies",
                "description": "Watch Ladies Gold",
                "sku": "watch123",
                "price": 20000,
                "quantity": 1,
                "image": None,
                "shippingCost": 0,
                "trackingUrl": "https://www.example.com"
            }],
            "udf1": "null",
            "udf2": "null",
            "udf3": "null",
            "udf4": "null",
            "udf5": "null"
        }
    }

    def setUp(self):
        super().setUp()
        self.test_string = "Test String"
        self.test_bytes = b"Test String"
        self.test_bytearray = bytearray(b"Test String")

    def test_utils_to_bytes__from_string(self):
        bytes_of_test_string = _to_bytes(self.test_string)
        self.assertEqual(type(bytes_of_test_string), bytes)

    def test_utils_to_bytes__from_bytes(self):
        bytes_of_test_bytes = _to_bytes(self.test_bytes)
        self.assertEqual(type(bytes_of_test_bytes), bytes)

    def test_utils_to_string__from_string(self):
        string_of_test_string = _to_string(self.test_string)
        self.assertEqual(type(string_of_test_string), str)

    def test_utils_to_string__from_bytearray(self):
        string_of_test_bytearray = _to_string(self.test_bytearray)
        self.assertEqual(type(string_of_test_bytearray), str)

    def test_utils_verify_signature(self):
        test_key = "key_12345678"
        test_body = "body"
        expected_signature = 'dc35f39ca2a088e52aa9833fd897a292133dbb2ab644c6076cb7f13540321f79'
        with self.assertRaises(InvalidSignatureError):
            verify_signature(test_key, test_body, expected_signature)

    def test_utils_verify_signature__invalid(self):
        test_key = "key_12345678"
        test_body = "body"
        expected_signature = 'invalid_signature'
        with self.assertRaises(InvalidSignatureError):
            verify_signature(test_key, test_body, expected_signature)

    @mock.patch('checkout_sdk.webhooks.utils.verify_signature')
    def test_utils_parse(self, verify_signature):
        event = parse(str(self.EVENT_REQUEST_BODY), 'secret_key', 'signature')
        self.assertEqual(type(event), Event)
        self.assertEqual(event.event_type, self.EVENT_REQUEST_BODY['eventType'])
        self.assertEqual(event.id, self.EVENT_REQUEST_BODY['message']['id'])