import re
import datetime
import checkout_sdk
import pprint

from checkout_sdk import errors, constants
from checkout_sdk import Currency, PaymentType
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
        if currency is not None and type(currency) is not str:
            raise TypeError('Currency should be a string.')
        if payment_type is not None and type(payment_type) is str and not PaymentType.has_value(payment_type):
            raise ValueError('Invalid payment type.')
        if payment_type is not None and type(payment_type) is not str:
            raise TypeError('Payment type should be a string.')
        if reference is not None and type(reference) is not str:
            raise TypeError('Reference must be a string.')

    @classmethod
    def validate_and_set_dynamic_class_attribute(cls, arg, clazz,
                                                 type_err_msg, missing_arg_err_msg=None):
        if arg is None and missing_arg_err_msg is not None:
            raise ValueError(missing_arg_err_msg)

        if arg is None or isinstance(arg, dict):
            return arg
        elif issubclass(clazz, RequestDTO) and isinstance(arg, clazz):
            return arg.get_dict()
        else:
            raise TypeError(
                '{} Please provide a dictionary or an instance of a RequestDTO subclass.'
                .format(type_err_msg))

    @classmethod
    def validate_and_set_dynamic_boolean_attribute(cls, arg, type_err_msg, missing_arg_err_msg=None):
        if arg is None and missing_arg_err_msg is not None:
            raise ValueError(missing_arg_err_msg)

        if arg is None or isinstance(arg, dict):
            return arg
        elif type(arg) is bool:
            return {'enabled': arg}
        else:
            raise TypeError(
                '{} Please provide a dictionary or a boolean value.'
                .format(type_err_msg))
