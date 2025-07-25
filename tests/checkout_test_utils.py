from __future__ import absolute_import

import logging
import time
import uuid
from pathlib import Path

from checkout_sdk.common.common import Address, Phone, CustomerRequest, AccountHolder
from checkout_sdk.common.enums import Country, AccountHolderType
from checkout_sdk.exception import CheckoutException, CheckoutApiException
from checkout_sdk.payments.payments import Payer, PaymentRecipient

NAME = 'Integration Test'
FIRST_NAME = 'Integration'
LAST_NAME = 'Test'
REFERENCE = 'Reference'
DESCRIPTION = 'Description'
SUCCESS_URL = 'https://testing.checkout.com/sucess'
FAILURE_URL = 'https://testing.checkout.com/failure'
PAYEE_NOT_ONBOARDED = 'payee_not_onboarded'
APM_SERVICE_UNAVAILABLE = 'apm_service_unavailable'
APM_CURRENCY_NOT_SUPPORTED = 'currency_not_supported'

_logger = logging.getLogger('checkout')


def retriable(callback, predicate=None, timeout=2, **kwargs):
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
        time.sleep(timeout)
    raise CheckoutException('Max attempts reached!')


def check_error_item(callback, error_item: str, **kwargs):
    try:
        callback(**kwargs)
    except CheckoutApiException as err:
        assert error_item in err.error_details, f"\n Expected: {error_item} " \
                                                f"\n Was actually: {', '.join(map(str, err.error_details))}"


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
    _address.address_line2 = 'max_10_c__'
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


def account_holder() -> AccountHolder:
    _account_holder = AccountHolder()
    _account_holder.type = AccountHolderType.INDIVIDUAL
    _account_holder.first_name = 'John'
    _account_holder.last_name = 'Doe'
    _account_holder.billing_address = address()
    _account_holder.phone = phone()
    _account_holder.account_name_inquiry = False
    return _account_holder


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
    expiry_year: int = 2030
    cvv: str = '100'


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_payer():
    payer = Payer()
    payer.email = random_email()
    payer.name = NAME
    payer.document = '53033315550'
    return payer


def get_payment_recipient():
    recipient = PaymentRecipient()
    recipient.account_number = '123456789'
    recipient.dob = '1985-05-18'
    recipient.first_name = 'IT'
    recipient.last_name = 'Testing'
    recipient.zip = '12345'
    recipient.country = Country.ES
    return recipient
