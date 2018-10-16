import unittest
import os
import tests
import json

import checkout_sdk as sdk

from http import HTTPStatus
from tests.base import CheckoutSdkTestCase
from checkout_sdk import Utils, errors
from checkout_sdk.common import HttpResponse
from checkout_sdk.payments import Customer


class UtilsTests(CheckoutSdkTestCase):
    VALID_ID = 'id'
    INVALID_ID = False

    def test_validate_id(self):
        try:
            Utils.validate_id(self.VALID_ID)
        except Exception:
            self.fail(
                'Utils.validate_payment_id raised an exception unexpectedly.')

    def test_validate_id_with_missing_id(self):
        with self.assertRaises(ValueError):
            Utils.validate_id(None)

    def test_validate_id_with_wrong_id_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_id(self.INVALID_ID)

    def test_validate_dynamic_attribute_dict(self):
        try:
            Utils.validate_dynamic_attribute({
                'key': 'value'
            }, None, None)
        except Exception:
            self.fail(
                'Utils.validate_dynamic_attribute raised an exception unexpectedly for a dictionary.')

    def test_validate_dynamic_attribute_class(self):
        try:
            Utils.validate_dynamic_attribute(Customer(), Customer, None)
        except Exception:
            self.fail(
                'Utils.validate_dynamic_attribute raised an exception unexpectedly for a valid class.')

    def test_validate_dynamic_attribute_with_missing_value(self):
        with self.assertRaises(ValueError):
            Utils.validate_dynamic_attribute(None, None, None, 'value error')

    def test_validate_dynamic_attribute_with_wrong_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_dynamic_attribute(
                False, Customer, 'type error')

    def test_validate_transaction(self):
        try:
            Utils.validate_transaction(
                100, sdk.Currency.USD, sdk.PaymentType.Recurring)
        except Exception:
            self.fail(
                'Utils.validate_transaction raised an exception unexpectedly when using enums.')

    def test_validate_transaction_without_enums(self):
        try:
            Utils.validate_transaction(100, 'eur', 'Regular')
        except Exception:
            self.fail(
                'Utils.validate_transaction raised an exception unexpectedly when not using enums')

    def test_validate_transaction_fails_with_missing_amount(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(None)

    def test_validate_transaction_fails_with_negative_amount(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(-5)

    def test_validate_transaction_fails_with_wrong_amount_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction('amount')

    def test_validate_transaction_fails_with_bad_currency(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(100, 'xxx')

    def test_validate_transaction_fails_with_wrong_currency_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, False)

    def test_validate_transaction_fails_with_bad_payment_type(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(100, 'usd', 'invalid')

    def test_validate_transaction_fails_with_wrong_payment_type_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, 'usd', False)

    def test_validate_transaction_fails_with_wrong_payment_reference_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, 'usd', 2, False)

    def test_is_pending_flow(self):
        http_response = HttpResponse(HTTPStatus.ACCEPTED, None, {}, 0)
        self.assertTrue(Utils.is_pending_flow(http_response))
