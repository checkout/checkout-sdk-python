from __future__ import absolute_import

import pytest

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.sessions.sessions import (
    PaymentSessionsRequest,
    PaymentSessionWithPaymentRequest,
    SubmitPaymentSessionRequest,
    SessionBilling,
    BillingAddress,
    BillingPhone,
    Item
)
from checkout_sdk.payments.payments import ThreeDsRequest
from tests.checkout_test_utils import assert_response


def test_should_create_payment_sessions(default_api):
    request = create_payment_sessions_request()

    response = default_api.payment_sessions.create_payment_sessions(request)

    assert_response(response,
                    'id',
                    '_links',
                    '_links.self')


@pytest.mark.skip(reason='use on demand')
def test_should_create_payment_session_with_payment(default_api):
    request = create_payment_session_with_payment_request()

    response = default_api.payment_sessions.create_payment_session_with_payment(request)

    assert_response(response,
                    'id',
                    'status',
                    'amount',
                    'currency',
                    '_links')


@pytest.mark.skip(reason='use on demand')
def test_should_submit_payment_session(default_api):
    # First create a payment session
    payment_session_request = create_payment_sessions_request()
    payment_session_response = default_api.payment_sessions.create_payment_sessions(payment_session_request)

    # Then submit a payment for that session
    submit_request = create_submit_payment_session_request()
    session_id = payment_session_response.id

    response = default_api.payment_sessions.submit_payment_session(session_id, submit_request)

    assert_response(response,
                    'id',
                    'status',
                    '_links')


def create_payment_sessions_request():
    billing_address = BillingAddress()
    billing_address.country = 'GB'
    billing_address.address_line1 = '123 High Street'
    billing_address.city = 'London'
    billing_address.zip = 'W1K 1LB'

    billing_phone = BillingPhone()
    billing_phone.country_code = '44'
    billing_phone.number = '7123456789'

    billing = SessionBilling()
    billing.address = billing_address
    billing.phone = billing_phone

    customer = CustomerRequest()
    customer.name = 'John Smith'
    customer.email = 'john.smith@example.com'

    request = PaymentSessionsRequest()
    request.amount = 2000
    request.currency = Currency.GBP
    request.reference = 'ORD-123A'
    request.billing = billing
    request.customer = customer
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'

    return request


def create_payment_session_with_payment_request():
    billing_address = BillingAddress()
    billing_address.country = 'GB'
    billing_address.address_line1 = '123 High Street'
    billing_address.city = 'London'
    billing_address.zip = 'W1K 1LB'

    billing_phone = BillingPhone()
    billing_phone.country_code = '44'
    billing_phone.number = '7123456789'

    billing = SessionBilling()
    billing.address = billing_address
    billing.phone = billing_phone

    customer = CustomerRequest()
    customer.name = 'John Smith'
    customer.email = 'john.smith@example.com'

    request = PaymentSessionWithPaymentRequest()
    request.session_data = 'session_data_token_example'
    request.amount = 2000
    request.currency = Currency.GBP
    request.reference = 'ORD-123B'
    request.billing = billing
    request.customer = customer
    request.success_url = 'https://example.com/payments/success'
    request.failure_url = 'https://example.com/payments/failure'

    return request


def create_submit_payment_session_request():
    three_ds = ThreeDsRequest()
    three_ds.enabled = True
    three_ds.attempt_n3d = False

    item = Item()
    item.name = 'Test Product'
    item.quantity = 1
    item.unit_price = 2000

    request = SubmitPaymentSessionRequest()
    request.session_data = 'session_data_token_example'
    request.amount = 2000
    request.reference = 'ORD-123C'
    request.items = [item]
    request.three_ds = three_ds
    request.ip_address = '90.197.169.245'

    return request
