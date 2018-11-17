import re
import datetime
import checkout_sdk
import pprint

from http import HTTPStatus
from checkout_sdk import errors, constants
from checkout_sdk import Currency, PaymentType, ChargeMode


class Utils:
    @classmethod
    def validate_id(cls, id):
        if id is None:
            raise ValueError('Invalid Id.')
        if type(id) is not str:
            raise TypeError('Id should be of string type.')

    @classmethod
    def validate_dynamic_attribute(cls, attribute, clazz, type_err_msg, missing_value_err_msg=None):
        if missing_value_err_msg is not None and attribute is None:
            raise ValueError(missing_value_err_msg)
        if attribute is not None and not (isinstance(attribute, dict) or isinstance(attribute, clazz)):
            raise TypeError(
                '{} Please provide a dictionary or valid class instance.'.format(type_err_msg))
