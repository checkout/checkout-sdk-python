import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import HttpClient, Config, HttpMethod
from tests.base import CheckoutSdkTestCase
from enum import Enum

from checkout_sdk.payments import (
    PaymentsClient,
    CardSource,
    Customer,
    ThreeDS
)
from checkout_sdk.payments.responses import (
    ThreeDSEnrollment,
    Customer as CustomerResponse,
    Payment,
    PaymentPending,
    PaymentProcessed
)
from checkout_sdk.common import Address, Phone


class PaymentsClientTests(CheckoutSdkTestCase):
    REFERENCE = 'REF_01'
    AMOUNT = 1000
    CURRENCY = sdk.Currency.USD
    CUSTOMER_EMAIL = 'test@user.com'
    CUSTOMER_NAME = 'Test User'
    CARD_NUMBER = '4242424242424242'
    CARD_EXPIRY_MONTH = 9
    CARD_EXPIRY_YEAR = 2025
    CARD_CVV = '100'
    BILLING_LINE_1 = '1 New Street'
    BILLING_CITY = 'London'
    BILLING_ZIP = 'W1'
    BILLING_COUNTRY = 'GB'
    PHONE_COUNTRY_CODE = '+44'
    PHONE_NUMBER = '02999999999'

    def setUp(self):
        super().setUp()
        self.http_client = HttpClient(Config())
        self.client = PaymentsClient(self.http_client)

    def tearDown(self):
        super().tearDown()
        self.http_client.close_session()

    def test_bad_payment_response_init(self):
        with self.assertRaises(TypeError):
            Payment(None, None)

    def test_payments_client_full_card_non_3ds_auth_request_with_classes(self):
        payment = self.auth_card()
        self.assert_payment_response(payment, PaymentProcessed, False)
        self.assert_customer(payment.customer)

    def test_payments_client_full_card_3ds_auth_request_with_classes(self):
        self.assert_payment_pending_response(self.auth_card(True, False))

    def test_payments_client_full_card_3ds_auth_request_with_dictionary(self):
        self.assert_payment_pending_response(self.auth_card(True, True))

    def auth_card(self, threeds=False, dict_format=False):
        return self.client.request(
            source=self.get_card_source(dict_format=dict_format),
            amount=self.AMOUNT,
            currency=self.CURRENCY,
            reference=self.REFERENCE,
            customer={
                'email': self.CUSTOMER_EMAIL,
                'name': self.CUSTOMER_NAME
            } if dict_format else Customer(email=self.CUSTOMER_EMAIL,
                                           name=self.CUSTOMER_NAME),
            threeds={
                'enabled': threeds
            } if dict_format else threeds
        )

    def get_card_source(self, dict_format=False):
        return {
            'type': 'card',
            'number': self.CARD_NUMBER,
            'expiry_month': self.CARD_EXPIRY_MONTH,
            'expiry_year': self.CARD_EXPIRY_YEAR,
            'cvv': self.CARD_CVV,
            'billing_address': {
                'address_line1': self.BILLING_LINE_1,
                'city': self.BILLING_CITY,
                'zip': self.BILLING_ZIP,
                'country': self.BILLING_COUNTRY
            },
            'phone': {
                'country_code': self.PHONE_COUNTRY_CODE,
                'number': self.PHONE_NUMBER
            }
        } if dict_format else CardSource(
            number=self.CARD_NUMBER,
            expiry_month=self.CARD_EXPIRY_MONTH,
            expiry_year=self.CARD_EXPIRY_YEAR,
            cvv=self.CARD_CVV,
            billing_address=Address(
                address_line1=self.BILLING_LINE_1,
                city=self.BILLING_CITY,
                zip=self.BILLING_ZIP,
                country=self.BILLING_COUNTRY
            ),
            phone=Phone(
                country_code=self.PHONE_COUNTRY_CODE,
                number=self.PHONE_NUMBER
            )
        )

    def assert_payment_pending_response(self, payment):
        self.assert_payment_response(payment, PaymentPending, True)
        self.assert_customer(payment.customer)
        # 3DS
        self.assertTrue(isinstance(payment.threeds, ThreeDSEnrollment))
        self.assertTrue(payment.requires_redirect)
        self.assertTrue(payment.redirect_link is not None)

    def assert_payment_response(self, payment, clazz=Payment, is_pending=False):
        self.assertTrue(isinstance(payment, clazz))
        # Resource
        self.assertIsNotNone(payment.request_id)
        self.assertTrue(payment.links is not None and len(payment.links) > 0)
        # PaymentResponse
        self.assertTrue(type(payment.id) is str)
        self.assertTrue(type(payment.status) is str)
        self.assertTrue(payment.is_pending == is_pending)

    def assert_customer(self, customer):
        self.assertTrue(isinstance(customer, CustomerResponse))
        self.assertIsNotNone(customer.id)
        self.assertTrue(customer.name == self.CUSTOMER_NAME)
        self.assertTrue(customer.email == self.CUSTOMER_EMAIL)
