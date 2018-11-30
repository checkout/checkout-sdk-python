import re
import datetime
import checkout_sdk
import pprint

from http import HTTPStatus
from checkout_sdk import errors, constants
from checkout_sdk import Currency, PaymentType, ChargeMode
from checkout_sdk.common import RequestDTO


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

    @classmethod
    def validate_and_set_dynamic_attribute(cls, arg, clazz, allow_boolean,
                                           type_err_msg, missing_arg_err_msg=None):
        if arg is None and missing_arg_err_msg is not None:
            raise ValueError(missing_arg_err_msg)

        if arg is None or isinstance(arg, dict):
            return arg

        instance = None
        if issubclass(clazz, RequestDTO):
            # Some classes can be set via a bool value as shortcut
            if allow_boolean and type(arg) is bool:
                instance = clazz(enabled=arg)
            elif isinstance(arg, clazz):
                instance = arg

        if instance is None:
            raise TypeError(
                '{} Please provide a dictionary or a subclass RequestDTO with matching instance.'
                .format(type_err_msg))

        return instance.get_dict()
