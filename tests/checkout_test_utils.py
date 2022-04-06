from __future__ import absolute_import

import logging
import time
import uuid
from pathlib import Path

from checkout_sdk.common.common import Address, Phone, CustomerRequest
from checkout_sdk.common.enums import Country
from checkout_sdk.exception import CheckoutException, CheckoutApiException

NAME = 'Integration Test'
FIRST_NAME = 'Integration'
LAST_NAME = 'Test'
SUCCESS_URL = 'https://testing.checkout.com/sucess'
FAILURE_URL = 'https://testing.checkout.com/failure'

_logger = logging.getLogger('checkout')


def retriable(callback, predicate=None, **kwargs):
    current_attempt = 1
    max_attempts = 10
    while current_attempt <= max_attempts:
        try:
            response = callback(**kwargs)
            if predicate is None:
                return response
            if predicate(response):
                return response
        except CheckoutApiException as ex:
            _logger.warning(
                'Request/Predicate failed with error ({}) - retry ({})/({})'.format(ex, current_attempt, max_attempts))
        current_attempt += 1
        time.sleep(2)
    raise CheckoutException('Max attempts reached!')


def assert_response(obj, *argv: str):
    assert obj is not None
    for prop in argv:
        if prop.__contains__('.'):
            # 'a.b.c' to 'a','b','c'
            props = prop.split('.')
            # value('a')
            nested_prop = getattr(obj, props[0])
            # collect to 'b.c'
            joined = str.join('.', props[1:])
            assert_response(nested_prop, joined)
        else:
            assert hasattr(obj, prop) is not False


def address() -> Address:
    _address = Address()
    _address.address_line1 = 'CheckoutSdk.com'
    _address.address_line2 = '90 Tottenham Court Road'
    _address.city = 'London'
    _address.state = 'London'
    _address.zip = 'W1T 4TJ'
    _address.country = Country.GB
    return _address


def phone() -> Phone:
    _phone = Phone()
    _phone.country_code = '44'
    _phone.number = '020222333'
    return _phone


def new_uuid() -> str:
    return str(uuid.uuid4())


def random_email() -> str:
    return new_uuid() + '@checkout.com'


def new_idempotency_key() -> str:
    return 'ik-' + new_uuid()


def common_customer_request() -> CustomerRequest:
    request = CustomerRequest()
    request.email = random_email()
    request.name = 'Name'
    return request


class VisaCard:
    name: str = 'Checkout Test'
    number: str = '4242424242424242'
    expiry_month: int = 6
    expiry_year: int = 2025
    cvv: str = '100'


def get_project_root() -> Path:
    return Path(__file__).parent.parent
