import unittest
import os
import tests
import json

import checkout_sdk as sdk

from http import HTTPStatus
from tests.base import CheckoutSdkTestCase
from checkout_sdk import errors, Utils
from checkout_sdk.common import HttpResponse, Address


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
            Utils.validate_dynamic_attribute(Address(), Address, None)
        except Exception:
            self.fail(
                'Utils.validate_dynamic_attribute raised an exception unexpectedly for a valid class.')

    def test_validate_dynamic_attribute_with_missing_value(self):
        with self.assertRaises(ValueError):
            Utils.validate_dynamic_attribute(None, None, None, 'value error')

    def test_validate_dynamic_attribute_with_wrong_type(self):
        with self.assertRaises(TypeError):
            Utils.validate_dynamic_attribute(
                False, Address, 'type error')
