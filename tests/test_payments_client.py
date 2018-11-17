import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import HttpClient, Config, HttpMethod
from tests.base import CheckoutSdkTestCase
from enum import Enum

from checkout_sdk.payments import PaymentsClient, CardSource, Customer, ThreeDS
from checkout_sdk.payments.responses import ThreeDSEnrollment, Customer as CustomerResponse, Payment, PaymentPending, PaymentProcessed
from checkout_sdk.common import Address, Phone


class PaymentsClientTests(CheckoutSdkTestCase):
    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_payment_response_init(self):
        with self.assertRaises(TypeError):
            Payment(False)

    def test_payments_client_full_card_3ds_auth_request_with_classes(self):
        payment = self.auth_card(True)

        self.assert_payment_response(payment, PaymentPending, True)
        # PaymentPending
        self.assertTrue(isinstance(payment.customer, CustomerResponse))
        self.assertTrue(type(payment.customer.id) is str)
        self.assertTrue(payment.customer.name == 'Test User')
        self.assertTrue(payment.customer.email == 'test@user.com')
        # 3DS
        self.assertTrue(isinstance(payment.threeds, ThreeDSEnrollment))
        self.assertTrue(payment.requires_redirect)
        self.assertTrue(payment.redirect_link is not None)

    def auth_card(self, threeds=False):
        return self.client.request(
            source=CardSource(
                number='4242424242424242',
                expiry_month=9,
                expiry_year=2025,
                cvv='100',
                billing_address=Address(
                    address_line1='1 New Street',
                    city='London',
                    zip='W1'
                ),
                phone=Phone(
                    country_code='+44',
                    number='7900900900'
                )
            ),
            amount=1000,
            currency=sdk.Currency.USD,
            payment_type=sdk.PaymentType.Regular,
            reference='REF_X01',
            customer=Customer(email='test@user.com', name='Test User'),
            threeds=ThreeDS(enabled=True) if threeds else None
        )

    def assert_payment_response(self, payment, clazz=Payment, is_pending=False):
        self.assertTrue(isinstance(payment, clazz))
        # Resource
        self.assertTrue(payment.links is not None and len(payment.links) > 0)
        # PaymentResponse
        self.assertTrue(type(payment.id) is str)
        self.assertTrue(type(payment.status) is str)
        self.assertTrue(type(payment.status) is str)
        self.assertTrue(payment.is_pending == is_pending)
