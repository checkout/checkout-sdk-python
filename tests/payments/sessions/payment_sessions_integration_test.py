from __future__ import absolute_import

from checkout_sdk.common.common import CustomerRequest
from checkout_sdk.common.enums import Currency
from checkout_sdk.payments.sessions.sessions import PaymentSessionsRequest, Billing
from tests.checkout_test_utils import assert_response, address


def test_should_create_payment_sessions(default_api):
    request = create_payment_sessions_request()

    response = default_api.sessions.create_payment_sessions(request)

    assert_response(response,
                    'id',
                    '_links',
                    '_links.self')


def create_payment_sessions_request():
    billing = Billing()
    billing.address = address()

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
