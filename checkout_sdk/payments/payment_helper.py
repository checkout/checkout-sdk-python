import re
import datetime
import checkout_sdk
import pprint

from http import HTTPStatus
from checkout_sdk import errors, constants
from checkout_sdk import Currency, PaymentType, ChargeMode, Utils
from checkout_sdk.payments import ThreeDS


class PaymentHelper:
    @classmethod
    def validate_transaction(cls, amount, currency=None, payment_type=None, reference=None):
        if amount is None or (type(amount) is int and amount < 0):
            raise ValueError('Amount must be greater or equal to zero.')
        if type(amount) is not int:
            raise TypeError('Amount must be an integer.')
        if currency is not None and type(currency) is str and not Currency.has_value(currency):
            raise ValueError('Invalid currency.')
        if currency is not None and not (isinstance(currency, Currency) or type(currency) is str):
            raise TypeError(
                'Currency should be of the correct enum type or a string.')
        if payment_type is not None and type(payment_type) is str and not PaymentType.has_value(payment_type):
            raise ValueError('Invalid payment type.')
        if payment_type is not None and not (isinstance(payment_type, PaymentType) or type(payment_type) is str):
            raise TypeError(
                'Payment type should be of the correct enum type or a string.')
        if reference is not None and type(reference) is not str:
            raise TypeError('Reference must be a string.')

    @classmethod
    def validate_and_set_threeds(cls, threeds):
        # some sugar on ThreeDS
        if type(threeds) is bool:
            return ThreeDS(enabled=threeds)
        else:
            Utils.validate_dynamic_attribute(
                threeds, clazz=ThreeDS, type_err_msg='Invalid 3DS.')
            return threeds

    @classmethod
    def is_pending_flow(cls, http_response):
        return http_response.status == HTTPStatus.ACCEPTED
