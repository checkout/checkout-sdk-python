import re
import datetime
import checkout_sdk
import pprint

from http import HTTPStatus
from checkout_sdk import errors, constants
from checkout_sdk import Currency, PaymentType, ChargeMode


class Validator:
    @classmethod
    def validate_id(cls, id):
        if id is None:
            raise ValueError('Invalid Id.')
        if type(id) is not str:
            raise TypeError('Id should be of string type.')

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

    # Some classes can be set via a bool value as shortcut
    @classmethod
    def validate_and_set_boolean_shortcut(cls, attribute, clazz, type_err_msg):
        if type(attribute) is bool:
            return clazz(enabled=attribute)
        else:
            cls.validate_dynamic_attribute(
                attribute, clazz=clazz, type_err_msg=type_err_msg)
            return attribute

    @classmethod
    def validate_dynamic_attribute(cls, attribute, clazz, type_err_msg, missing_value_err_msg=None):
        if missing_value_err_msg is not None and attribute is None:
            raise ValueError(missing_value_err_msg)
        if attribute is not None and not (isinstance(attribute, dict) or isinstance(attribute, clazz)):
            raise TypeError(
                '{} Please provide a dictionary or valid class instance.'.format(type_err_msg))
