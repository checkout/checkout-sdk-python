from unittest.mock import Mock, MagicMock

from checkout_sdk import HttpClient, Config
from checkout_sdk.cards import CardsClient, CardResponse
from tests.base import CheckoutSdkTestCase


class CardsClientTests(CheckoutSdkTestCase):
    RESPONSE_GET_CARD_BODY = {
        "customerId": "cust_9E07EFB6-32E0-4D6C-B5AD-6EE403BA3F97",
        "expiryMonth": "06",
        "expiryYear": "2018",
        "billingDetails": {
            "addressLine1": "27 Acacia Tree Street",
            "addressLine2": "Apartment 15",
            "postcode": "01072",
            "country": "US",
            "city": "Shutesbury",
            "state": "Massachusetts",
            "phone": {
                "countryCode": "1",
                "number": "111 222-333"
            }
        },
        "id": "card_49E69E61-8E35-40E0-AA10-B0B15F198275",
        "last4": "4242",
        "bin": "424242",
        "paymentMethod": "Visa",
        "fingerprint": "F639CAB2745BEE4140BF86DF6B6D6E255C5945AAC3788D923FA047EA4C208622",
        "name": "Miss Matt Quigley"
    }

    RESPONSE_GET_CARDS_BODY = {
        "count": 2,
        "data": [
            {
                "customerId": "cust_291262B9-FEF1-41AE-A593-311F481D3A85",
                "expiryMonth": "06",
                "expiryYear": "2018",
                "billingDetails": {
                    "addressLine1": "27 Acacia Tree Street",
                    "addressLine2": "Apartment 15",
                    "postcode": "01072",
                    "country": "US",
                    "city": "Shutesbury",
                    "state": "Massachusetts",
                    "phone": {
                        "countryCode": "1",
                        "number": "111 222-333"
                    }
                },
                "id": "card_99CB8B47-A2C3-4A35-8EDC-4498B60B0FE8",
                "last4": "5678",
                "bin": "424242",
                "paymentMethod": "Visa",
                "fingerprint": "F639CAB2745BEE4140BF86DF6B6D6E255C5945AAC3788D923FA047EA4C208622",
                "name": "Sarah Mitchell",
                "avsCheck": "AE7"
            },
            {
                "customerId": "cust_291262B9-FEF1-41AE-A593-311F481D3A85",
                "expiryMonth": "6",
                "expiryYear": "2018",
                "billingDetails": {
                    "addressLine1": "27 Acacia Tree Street",
                    "addressLine2": "Apartment 15",
                    "postcode": "01072",
                    "country": "US",
                    "city": "Shutesbury",
                    "state": "Massachusetts",
                    "phone": {
                        "countryCode": "1",
                        "number": "111 222-333"
                    }
                },
                "id": "card_0A7997B6-6B7C-4544-96B9-743AA446365C",
                "last4": "1234",
                "bin": "424242",
                "paymentMethod": "Visa",
                "fingerprint": "F639CAB2745BEE4140BF86DF6B6D6E255C5945AAC3788D923FA047EA4C208622",
                "name": "Sarah Mitchell"
            }
        ]
    }

    RESPONSE_REMOVE_CARD_BODY = {
        "message": "ok"
    }

    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.client = CardsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_card_response_init(self):
        with self.assertRaises(TypeError):
            CardResponse(False)

    def set_mock_response(self, name, headers, body, status_code=200):
        response = Mock(name=name, status_code=status_code, headers=headers)
        response.json.return_value = body
        response.body = body
        response.status = status_code
        self.http_client._session.request = MagicMock(return_value=response)

    def test_cards_client_get_card_request(self):
        self.set_mock_response(
            name='get_card',
            body=self.RESPONSE_GET_CARD_BODY,
            headers=self.http_client.headers
        )
        card_response = self.client.get_card(
            customer_id='cust_0F0AFC8B-26E7-4892-AF1D-6C1D0AD83A3E',
            card_id='card_96CF7590-9D41-40AE-87C8-86852F27C52A'
        )

        self.assertEqual(card_response.http_response.status, 200)
        self.assertIsNotNone(card_response.card.id)

    def test_cards_client_get_cards_request(self):
        self.set_mock_response(
            name='get_cards',
            body=self.RESPONSE_GET_CARDS_BODY,
            headers=self.http_client.headers
        )
        cards_response = self.client.get_cards(
            customer_id='cust_0F0AFC8B-26E7-4892-AF1D-6C1D0AD83A3E'
        )

        self.assertEqual(cards_response.http_response.status, 200)
        self.assertIsNotNone(cards_response.cards)
        self.assertEqual(len(cards_response.cards), 2)

    def test_cards_client_remove_card_request(self):
        self.set_mock_response(
            name='remove_card',
            body=self.RESPONSE_REMOVE_CARD_BODY,
            headers=self.http_client.headers
        )
        cards_response = self.client.remove_card(
            customer_id='cust_0F0AFC8B-26E7-4892-AF1D-6C1D0AD83A3E',
            card_id='card_96CF7590-9D41-40AE-87C8-86852F27C52A'
        )

        self.assertEqual(cards_response.http_response.status, 200)
