import unittest
import os
import tests
import json

import checkout_sdk as sdk

from checkout_sdk import Utils, errors
from tests.base import CheckoutSdkTestCase


class UtilsTests(CheckoutSdkTestCase):
    VALID_PAYMENT_ID = 'charge_test_ABCDEFGHIJ1234567890'
    INVALID_PAYMENT_ID = 'charge_invalid'
    CARD_ID = 'card_B43AAAAA-2AAA-4BBB-9CCC-19D4F4D4F4D4'
    TOKEN_ID = 'tok_A43BBBBB-BBBB-CCCC-DDDD-10DDFFD5F5D5'
    CUSTOMER_ID = 'cust_P43CCCCC-2BBB-4CCC-1ABC-111111111111'
    VALID_PAN = '4242424242424242'
    INVALID_PAN = '4242424242424241'

    def test_validate_payment_id(self):
        try:
            Utils.validate_payment_id(self.VALID_PAYMENT_ID)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_payment_id raised BadRequestError unexpectedly')

    def test_validate_invalid_payment_id(self):
        with self.assertRaises(errors.BadRequestError):
            Utils.validate_payment_id(self.INVALID_PAYMENT_ID)

    def test_validate_payment_source_card(self):
        try:
            Utils.validate_payment_source(self.CARD_ID)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_payment_source raised BadRequestError unexpectedly for a valid card id')

    def test_validate_payment_source_token(self):
        try:
            Utils.validate_payment_source(None, self.TOKEN_ID)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_payment_source raised BadRequestError unexpectedly for a valid token')

    def test_validate_transaction(self):
        try:
            Utils.validate_transaction(
                100, sdk.Currency.USD, sdk.PaymentType.Recurring)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_transaction raised BadRequestError unexpectedly with enums')

    def test_validate_transaction_without_enums(self):
        try:
            Utils.validate_transaction(100, 'eur', 2)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_transaction raised BadRequestError unexpectedly when not using enums')

    def test_validate_transaction_fails_with_bad_values(self):
        with self.assertRaises(errors.BadRequestError):
            Utils.validate_transaction(100, 'xxx', 5)

    def test_validate_customer(self):
        try:
            Utils.validate_customer(self.CUSTOMER_ID)
        except errors.BadRequestError:
            self.fail(
                'Utils.validate_customer raised BadRequestError unexpectedly for a valid customer id')

    def test_throw(self):
        with self.assertRaises(errors.BadRequestError):
            Utils.throw('message')

    def test_is_id(self):
        self.assertEqual(Utils.is_id(self.CARD_ID, 'card', False),
                         True, 'Card Id unexpectedly invalid')
        self.assertEqual(Utils.is_id(self.CUSTOMER_ID, 'cust',
                                     False), True, 'Customer Id unexpectedly invalid')
        self.assertEqual(Utils.is_id(
            self.VALID_PAYMENT_ID, 'charge_test', True), True, 'Charge Id unexpectedly invalid')
        self.assertEqual(Utils.is_id(self.CARD_ID, '...', False),
                         False, 'Card Id unexpectedly valid')
        self.assertEqual(Utils.is_id(self.CARD_ID, 'card', True),
                         False, 'Card Id unexpectedly valid')

    def test_is_number(self):
        self.assertEqual(Utils.is_number(5, 1, 10), True,
                         'Number unexpctedly out of range')
        self.assertEqual(Utils.is_number(5, 5, 5), True,
                         'Number unexpctedly out of range')
        self.assertEqual(Utils.is_number('5', 5, 5), True,
                         'Number unexpctedly out of range')
        self.assertEqual(Utils.is_number(10, 11, 15), False,
                         'Number unexpctedly in range')
        self.assertEqual(Utils.is_number(15, 11), True,
                         'Number unexpctedly out of range')
        self.assertEqual(Utils.is_number('ABC'), False,
                         '"ABC" is not a number')
        self.assertEqual(Utils.is_number(None), False,
                         'None type is not a number')

    def test_luhn_check(self):
        self.assertEqual(Utils.luhn_check(self.VALID_PAN),
                         True, 'PAN unexpected invalid')
        self.assertEqual(Utils.luhn_check(self.INVALID_PAN),
                         False, 'PAN unexpected valid')

    def test_mask_pan(self):
        self.assertEqual(Utils.mask_pan(self.VALID_PAN), '424242******4242')
