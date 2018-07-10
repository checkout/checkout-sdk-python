import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import HttpClient, Config, Utils
from checkout_sdk.payments import PaymentsClient
from tests.base import CheckoutSdkTestCase
from enum import Enum


class PaymentsClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_payments_client_full_card_auth_request(self):
        payment = self.auth_card()

        self.assertEqual(payment.http_response.status, 200)

        # test payment
        self.assertTrue(Utils.is_id(payment.id, short_id=True))
        self.assertTrue(payment.approved)
        self.assertEqual(payment.value, 100)
        self.assertEqual(payment.currency, 'USD')
        self.assertEqual(payment.track_id, 'ORDER-001-002')

        # test card
        self.assertTrue(Utils.is_id(payment.card.id), 'card')
        self.assertEqual(int(payment.card.expiryMonth), 6)
        self.assertEqual(int(payment.card.expiryYear), 2025)
        self.assertEqual(payment.card.last4, '4242')
        self.assertEqual(payment.card.name, 'Joe Smith')

        # test customer
        self.assertTrue(Utils.is_id(payment.customer.id, 'cust'))
        self.assertEqual(payment.customer.email, 'joesmith@gmail.com')

        # test other content from the http body
        body = payment.http_response.body

        self.assertEqual(body['card']['billingDetails']['city'], 'London')
        self.assertEqual(body['transactionIndicator'],
                         sdk.PaymentType.Recurring.value)  # pylint: disable = no-member
        self.assertEqual(body['udf1'], 'udf1')
        # below is also a test of snake >> camel casing.
        self.assertEqual(body['customerIp'], '8.8.8.8')
        self.assertEqual(body['products'][0]['price'], 2000)

    def test_payments_client_get_request(self):
        payment = self.auth_card()
        # get the previous auth request
        response = self.client.get(payment.id)

        self.assertEqual(response.http_response.status, 200)
        self.assertEqual(payment.id, response.id)
        # TODO: improve test to compare all GET value with previous Auth response values

    def test_payments_client_capture_full_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        response = self.client.capture(payment.id,
                                       track_id='ORDER-001-002-CAPTURE')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertTrue(Utils.is_id(response.id, short_id=True))
        self.assertTrue(Utils.is_id(response.original_id, short_id=True))
        self.assertEqual(payment.id, response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-CAPTURE')
        self.assertEqual(response.value, 150)
        self.assertTrue(response.approved)

    def test_payments_client_capture_partial_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        response = self.client.capture(payment.id, value=100,
                                       track_id='ORDER-001-002-CAPTURE')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertTrue(Utils.is_id(response.id, short_id=True))
        self.assertTrue(Utils.is_id(response.original_id, short_id=True))
        self.assertEqual(response.track_id, 'ORDER-001-002-CAPTURE')
        self.assertEqual(response.value, 100)
        self.assertTrue(response.approved)

    def test_payments_client_void_request(self):
        payment = self.auth_card()
        # void the previous auth request
        response = self.client.void(payment.id,
                                    track_id='ORDER-001-002-VOID')

        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertTrue(Utils.is_id(response.id, short_id=True))
        self.assertTrue(Utils.is_id(response.original_id, short_id=True))
        self.assertEqual(response.track_id, 'ORDER-001-002-VOID')
        self.assertTrue(response.approved)

    def test_payments_client_refund_full_amount_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      track_id='ORDER-001-002-CAPTURE')
        self.assertEqual(payment.id, capture.original_id)
        # refund the capture
        response = self.client.refund(capture.id,
                                      track_id='ORDER-001-002-REFUND')
        self.assertEqual(response.http_response.status, 200)
        # test payment
        self.assertTrue(Utils.is_id(response.id, short_id=True))
        self.assertTrue(Utils.is_id(response.original_id, short_id=True))
        self.assertEqual(capture.id, response.original_id)
        self.assertEqual(response.track_id, 'ORDER-001-002-REFUND')
        self.assertEqual(response.value, 150)
        self.assertTrue(response.approved)

    def test_payments_client_multiple_partial_refunds_request(self):
        payment = self.auth_card(value=150)
        # capture the previous auth request
        capture = self.client.capture(payment.id,
                                      track_id='ORDER-001-002-CAPTURE')
        self.assertEqual(payment.id, capture.original_id)
        # partial refund the capture
        response1 = self.client.refund(capture.id, value=50,
                                       track_id='ORDER-001-002-REFUND-1')
        self.assertTrue(response1.approved)
        self.assertEqual(response1.value, 50)

        response2 = self.client.refund(capture.id, value=80,
                                       track_id='ORDER-001-002-REFUND-2')
        self.assertTrue(response2.approved)
        self.assertEqual(response2.value, 80)

    def auth_card(self, value=None):
        # TODO: put test values into CONSTANTS where appropriate
        payment = self.client.request(
            card={
                'number': '4242424242424242',
                'expiryMonth': 6,
                'expiry_year': 2025,  # testing that snake_case is automatically converted
                'cvv': '100',
                'name': 'Joe Smith',
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
            value=value or 100,  # cents
            currency=sdk.Currency.USD,  # or 'usd'
            payment_type=sdk.PaymentType.Recurring,
            track_id='ORDER-001-002',
            customer='joesmith@gmail.com',
            udf1='udf1',
            customer_ip='8.8.8.8',
            products=[{
                "description": "Blue Medium",
                "name": "T-Shirt",
                "price": 2000,
                "quantity": 1,
                "shippingCost": 50,
                "sku": "tee123"
            }]
        )

        return payment
