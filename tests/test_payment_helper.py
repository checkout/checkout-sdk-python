import unittest
import os
import tests
import json

import checkout_sdk as sdk

from http import HTTPStatus
from tests.base import CheckoutSdkTestCase
from checkout_sdk import errors
from checkout_sdk.common import HttpResponse
from checkout_sdk.payments import PaymentHelper


class UtilsTests(CheckoutSdkTestCase):

    def test_validate_transaction(self):
        try:
            PaymentHelper.validate_transaction(
                100, sdk.Currency.USD, sdk.PaymentType.Recurring)
        except Exception:
            self.fail(
                'PaymentHelper.validate_transaction raised an exception unexpectedly when using enums.')

    def test_validate_transaction_without_enums(self):
        try:
            PaymentHelper.validate_transaction(100, 'eur', 'Regular')
        except Exception:
            self.fail(
                'PaymentHelper.validate_transaction raised an exception unexpectedly when not using enums')

    def test_validate_transaction_fails_with_missing_amount(self):
        with self.assertRaises(ValueError):
            PaymentHelper.validate_transaction(None)

    def test_validate_transaction_fails_with_negative_amount(self):
        with self.assertRaises(ValueError):
            PaymentHelper.validate_transaction(-5)

    def test_validate_transaction_fails_with_wrong_amount_type(self):
        with self.assertRaises(TypeError):
            PaymentHelper.validate_transaction('amount')

    def test_validate_transaction_fails_with_bad_currency(self):
        with self.assertRaises(ValueError):
            PaymentHelper.validate_transaction(100, 'xxx')

    def test_validate_transaction_fails_with_wrong_currency_type(self):
        with self.assertRaises(TypeError):
            PaymentHelper.validate_transaction(100, False)

    def test_validate_transaction_fails_with_bad_payment_type(self):
        with self.assertRaises(ValueError):
            PaymentHelper.validate_transaction(100, 'usd', 'invalid')

    def test_validate_transaction_fails_with_wrong_payment_type_type(self):
        with self.assertRaises(TypeError):
            PaymentHelper.validate_transaction(100, 'usd', False)

    def test_validate_transaction_fails_with_wrong_payment_reference_type(self):
        with self.assertRaises(TypeError):
            PaymentHelper.validate_transaction(100, 'usd', 2, False)

    def test_is_pending_flow(self):
        http_response = HttpResponse(HTTPStatus.ACCEPTED, None, {}, 0)
        self.assertTrue(PaymentHelper.is_pending_flow(http_response))
