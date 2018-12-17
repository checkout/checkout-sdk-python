import checkout_sdk as sdk

from tests.base import CheckoutSdkTestCase
from checkout_sdk import errors, Validator
from checkout_sdk.common import HTTPResponse


class ValidatorTests(CheckoutSdkTestCase):
    VALID_ID = 'id'
    INVALID_ID = False

    def test_validate_id(self):
        try:
            Validator.validate_id(self.VALID_ID)
        except Exception:
            self.fail(
                'Validator.validate_payment_id raised an exception unexpectedly.')

    def test_validate_id_with_missing_id(self):
        with self.assertRaises(ValueError):
            Validator.validate_id(None)

    def test_validate_id_with_wrong_id_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_id(self.INVALID_ID)

    def test_validate_complex_attribute(self):
        try:
            Validator.validate_complex_attribute({
                'key': 'value'
            }, None)
        except Exception:
            self.fail(
                'Validator.validate_complex_attribute raised an exception unexpectedly for a dictionary.')

    def test_validate_complex_attribute_with_missing_value(self):
        with self.assertRaises(ValueError):
            Validator.validate_complex_attribute(
                None, None, 'value error')

    def test_validate_complex_attribute_with_wrong_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_complex_attribute(
                False, 'type error')

    def test_validate_and_set_dynamic_attr_with_boolean_shortcut(self):
        try:
            Validator.validate_and_set_dynamic_attr(
                True, 'type error')
        except:
            self.fail(
                'Validator.validate_and_set_dynamic_attr raised an exception unexpectedly when using a boolean shortcut.')

    def test_validate_and_set_dynamic_attr_fails_without_required_attribute(self):
        with self.assertRaises(ValueError):
            Validator.validate_and_set_dynamic_attr(None, None, 'Value error')

    def test_validate_and_set_dynamic_attr_fails_with_bad_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_and_set_dynamic_attr(1, 'Type error')

    def test_validate_transaction(self):
        try:
            Validator.validate_transaction(
                100, sdk.Currency.USD, sdk.PaymentType.Recurring)
        except Exception:
            self.fail(
                'Validator.validate_transaction raised an exception unexpectedly when using enums.')

    def test_validate_transaction_without_enums(self):
        try:
            Validator.validate_transaction(100, 'eur', 'Regular')
        except Exception:
            self.fail(
                'Validator.validate_transaction raised an exception unexpectedly when not using enums')

    def test_validate_transaction_fails_with_missing_amount(self):
        with self.assertRaises(ValueError):
            Validator.validate_transaction(None)

    def test_validate_transaction_fails_with_negative_amount(self):
        with self.assertRaises(ValueError):
            Validator.validate_transaction(-5)

    def test_validate_transaction_fails_with_wrong_amount_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_transaction('amount')

    def test_validate_transaction_fails_with_bad_currency(self):
        with self.assertRaises(ValueError):
            Validator.validate_transaction(100, 'xxx')

    def test_validate_transaction_fails_with_wrong_currency_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_transaction(100, False)

    def test_validate_transaction_fails_with_bad_payment_type(self):
        with self.assertRaises(ValueError):
            Validator.validate_transaction(100, 'usd', 'invalid')

    def test_validate_transaction_fails_with_wrong_payment_type_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_transaction(100, 'usd', False)

    def test_validate_transaction_fails_with_wrong_payment_reference_type(self):
        with self.assertRaises(TypeError):
            Validator.validate_transaction(100, 'usd', 'Regular', False)

    def test_validate_source_type_fails_with_wrong_source_type_value(self):
        with self.assertRaises(ValueError):
            Validator.validate_and_set_source_type({
                "type": "bad_type"
            })

    def test_validate_source_type_with_valid_source_type(self):
        source = Validator.validate_and_set_source_type({
            "type": "card"
        })
        self.assertTrue(source['type'] == 'card')
