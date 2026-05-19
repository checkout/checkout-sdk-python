from __future__ import absolute_import

from checkout_sdk.payments.payments import ReversePaymentRequest
from tests.checkout_test_utils import new_uuid, assert_response, new_idempotency_key, retriable
from tests.payments.payments_test_utils import make_card_payment


# tests

def test_should_reverse_card_payment(default_api):
    payment_response = make_card_payment(default_api)

    reverse_request = build_reverse_payment_request()

    reverse_response = retriable(callback=default_api.payments.reverse_payment,
                                 payment_id=payment_response.id,
                                 reverse_payment_request=reverse_request)
    assert_reverse_response(reverse_response)


def test_should_reverse_card_payment_idempotently(default_api):
    payment_response = make_card_payment(default_api)

    reverse_request = build_reverse_payment_request()
    idempotency_key = new_idempotency_key()

    reverse_response_1 = retriable(callback=default_api.payments.reverse_payment,
                                   payment_id=payment_response.id,
                                   reverse_payment_request=reverse_request,
                                   idempotency_key=idempotency_key)
    assert_response(reverse_response_1)

    reverse_response_2 = retriable(callback=default_api.payments.reverse_payment,
                                   payment_id=payment_response.id,
                                   reverse_payment_request=reverse_request,
                                   idempotency_key=idempotency_key)
    assert_response(reverse_response_2)

    assert reverse_response_1.action_id == reverse_response_2.action_id


# common methods

def build_reverse_payment_request() -> ReversePaymentRequest:
    request = ReversePaymentRequest()
    request.reference = new_uuid()
    return request


def assert_reverse_response(response):
    assert_response(response,
                    'http_metadata',
                    'reference',
                    'action_id',
                    '_links')
