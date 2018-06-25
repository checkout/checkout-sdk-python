import unittest
import os
import tests
import json

import checkout_sdk as sdk
from checkout_sdk import HttpClient, Config
from checkout_sdk.payments import PaymentsClient
from tests.base import CheckoutSdkTestCase


class PaymentsClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(
            Config(api_base_url=tests.MOCK_API_BASE_URL))
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_payments_client_auth_request(self):
        try:
            response = self.client.request(
                card={
                    'number': '4242424242424242',
                    'expiryMonth': 6,
                    'expiryYear': 2018,
                    'cvv': '100'
                },
                value=100,  # cents
                currency=sdk.Currency.USD,  # or 'usd',
                payment_type=sdk.PaymentType.Recurring,
                customer='cust_3D34FB2D-A64A-4300-9B70-1D453D7BC3CE'
            )
            print(response)  # status, elapsed ms
        except sdk.errors.CheckoutSdkError as e:
            print(
                '{0.http_status} {0.error_code} {0.elapsed} {0.event_id} // {0.message}'.format(e))

        self.assertEqual(1, 1)
