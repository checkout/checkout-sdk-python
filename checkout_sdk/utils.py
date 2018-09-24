import re
import datetime
import checkout_sdk
import pprint

from checkout_sdk import errors, constants
from checkout_sdk.enums import Currency, PaymentType, ChargeMode

EMAIL_REGEX = re.compile(r'^.+@.+$', re.IGNORECASE)
PAYMENT_TOKEN_REGEX = re.compile(r'^pay_tok_', re.IGNORECASE)


class Utils:
    @classmethod
    def validate_id(cls, id):
        """Validates the payment id."""
        if id is None:
            raise ValueError('Invalid Payment/Charge Id.')
        if type(id) is not str:
            raise TypeError('Id should be of string type.')

    @classmethod
    def validate_payment_source(cls, card=None, token=None):
        """Validates card and token payment sources."""
        if card is None and token is None:
            raise ValueError(
                'Payment source missing. Please specify a valid card or token.')
        if card is not None and not (isinstance(card, dict) or type(card) is str):
            raise TypeError(
                'Invalid card source. Please provide a valid Card Id.')
        if token is not None and type(token) is not str:
            raise TypeError('Invalid token source.')

    @classmethod
    def validate_customer(cls, customer):
        if customer is None:
            raise ValueError(
                'Email or Customer Id is required when requesting a payment.')
        if type(customer) is not str:
            raise TypeError(
                'Customer should be of string type')

    @classmethod
    def is_email(cls, val):
        return EMAIL_REGEX.match(val) is not None

    @classmethod
    def validate_transaction(cls, value, currency=None, payment_type=None, charge_mode=None):
        if value is None or (type(value) is int and value < 0):
            raise ValueError('Value must be greater or equal to zero.')
        if type(value) is not int:
            raise TypeError('Value must be an integer.')
        if currency is not None and type(currency) is str and not Currency.has_value(currency):
            raise ValueError('Invalid currency.')
        if currency is not None and not (isinstance(currency, Currency) or type(currency) is str):
            raise TypeError(
                'Currency should be of the correct enum type or a string.')
        if payment_type is not None and type(payment_type) is int and not PaymentType.has_value(payment_type):
            raise ValueError('Invalid payment type.')
        if payment_type is not None and not (isinstance(payment_type, PaymentType) or type(payment_type) is int):
            raise TypeError(
                'Payment type should be of the correct enum type or an integer.')
        if charge_mode is not None and type(charge_mode) is int and not ChargeMode.has_value(charge_mode):
            raise ValueError('Invalid charge mode.')
        if charge_mode is not None and not (isinstance(charge_mode, ChargeMode) or type(charge_mode) is int):
            raise TypeError(
                'Charge mode should be of the correct enum type or an integer.')

    @classmethod
    def mask_pan(cls, pan):
        left, right = (6, 4)
        return pan[0:left].ljust(len(pan)-right, '*')+pan[-right:]

    @classmethod
    def verify_redirect_flow(cls, http_response):
        # this is how a 3D response is detected currently
        return http_response.body.get('redirectUrl') is not None \
            and PAYMENT_TOKEN_REGEX.match(http_response.body.get('id')) is not None
