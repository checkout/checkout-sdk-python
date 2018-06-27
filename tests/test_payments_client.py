import unittest
import os
import tests
import json

import checkout_sdk as sdk
from checkout_sdk import HttpClient, Config, Validator
from checkout_sdk.payments import PaymentsClient
from tests.base import CheckoutSdkTestCase


class PaymentsClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(
            Config(api_base_url=tests.MOCK_API_BASE_URL))
        #self.http_client = HttpClient(Config())
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_payments_client_full_card_auth_request(self):
        try:
            response = self.client.request(
                card={
                    'number': '4242424242424242',
                    'expiryMonth': 6,
                    'expiryYear': 2018,
                    'cvv': '100',
                    'billingDetails': {
                        'addressLine1': '1 London Street',
                        'postcode': 'W1',
                        'country': 'GB',
                        'city': 'London',
                        'state': 'Central London',
                        'phone': {
                            'countryCode': '44',
                            'number': '203 123 1234'
                        }
                    }
                },
                value=100,  # cents
                currency=sdk.Currency.USD,  # or 'usd'
                payment_type=sdk.PaymentType.Recurring,
                track_id='ORDER-001-002',
                customer='riazbordie@gmail.com',
                udf1='udf1',
                customerIp='8.8.8.8',
                products=[{
                    "description": "Blue Medium",
                    "name": "T-Shirt",
                    "price": 2000,
                    "quantity": 1,
                    "shippingCost": 50,
                    "sku": "tee123"
                }]
            )
            self.assertEqual(response.http_status, 200)
            self.assertTrue(Validator.is_id(
                response.body['card']['id'], 'card'))
            self.assertEqual(response.body['value'], 100)
            # expiry month and year return as string
            self.assertEqual(response.body['card']['expiryMonth'], '6')
            self.assertEqual(response.body['card']
                             ['billingDetails']['city'], 'London')
            self.assertEqual(response.body['transactionIndicator'], 2)
            self.assertEqual(response.body['udf1'], 'udf1')
            self.assertEqual(response.body['customerIp'], '8.8.8.8')
            self.assertEqual(response.body['products'][0]['price'], 2000)
        except sdk.errors.CheckoutSdkError as e:
            print(
                '{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))
