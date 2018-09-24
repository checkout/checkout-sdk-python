import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import Utils, errors
from tests.base import CheckoutSdkTestCase
from checkout_sdk import HttpResponse


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

    def test_validate_payment_source_card(self):
        try:
            Utils.validate_payment_source(self.VALID_ID)
        except Exception:
            self.fail(
                'Utils.validate_payment_source raised an exception unexpectedly for a valid card source.')

    def test_validate_payment_source_token(self):
        try:
            Utils.validate_payment_source(None, self.VALID_ID)
        except Exception:
            self.fail(
                'Utils.validate_payment_source raised an exception unexpectedly for a valid token.')

    def test_validate_payment_source_with_missing_source(self):
        with self.assertRaises(ValueError):
            Utils.validate_payment_source(None, None)

    def test_validate_payment_source_card_id_fails(self):
        with self.assertRaises(TypeError):
            Utils.validate_payment_source(self.INVALID_ID)

    def test_validate_payment_source_token_fails(self):
        with self.assertRaises(TypeError):
            Utils.validate_payment_source(None, self.INVALID_ID)

    def test_validate_customer_with_missing_id(self):
        with self.assertRaises(ValueError):
            Utils.validate_customer(None)

    def test_validate_customer_with_wrong_id_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_customer(self.INVALID_ID)

    def test_validate_transaction(self):
        try:
            Utils.validate_transaction(
                100, sdk.Currency.USD, sdk.PaymentType.Recurring, sdk.ChargeMode.NonThreeD)
        except Exception:
            self.fail(
                'Utils.validate_transaction raised an exception unexpectedly when using enums.')

    def test_validate_transaction_without_enums(self):
        try:
            Utils.validate_transaction(100, 'eur', 2, 1)
        except Exception:
            self.fail(
                'Utils.validate_transaction raised an exception unexpectedly when not using enums')

    def test_validate_transaction_fails_with_missing_value(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(None)

    def test_validate_transaction_fails_with_negative_value(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(-5)

    def test_validate_transaction_fails_with_wrong_value_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction('value')

    def test_validate_transaction_fails_with_bad_currency(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(100, 'xxx')

    def test_validate_transaction_fails_with_wrong_currency_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, False)

    def test_validate_transaction_fails_with_bad_payment_type(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(100, 'usd', 5)

    def test_validate_transaction_fails_with_wrong_payment_type_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, 'usd', False)

    def test_validate_transaction_fails_with_bad_charge_mode(self):
        with self.assertRaises(ValueError):
            Utils.validate_transaction(100, 'usd', 2, 10)

    def test_validate_transaction_fails_with_wrong_charge_mode_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_transaction(100, 'usd', 2, False)

    def test_verify_redirect_flow(self):
        http_response = HttpResponse(200, None, {
            'redirectUrl': 'http',
            'id': 'pay_tok_1'
        }, 0)
        self.assertTrue(Utils.verify_redirect_flow(http_response))
