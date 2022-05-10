from __future__ import absolute_import

from checkout_sdk.payments.payments_four import CaptureRequest
from tests.checkout_test_utils import new_uuid, assert_response, new_idempotency_key, retriable
from tests.payments.four.payments_four_test_utils import make_card_payment


def test_should_full_capture_card_payment(four_api):
    payment_response = make_card_payment(four_api)

    capture_request = CaptureRequest()
    capture_request.reference = new_uuid()

    capture_response = retriable(callback=four_api.payments.capture_payment,
                                 payment_id=payment_response.id,
                                 capture_request=capture_request)
    assert_response(capture_response,
                    'http_metadata',
                    'reference',
                    'action_id',
                    '_links')


def test_should_partially_capture_card_payment(four_api):
    payment_response = make_card_payment(four_api)

    capture_request = CaptureRequest()
    capture_request.reference = new_uuid()
    capture_request.amount = 5

    capture_response = retriable(callback=four_api.payments.capture_payment,
                                 payment_id=payment_response.id,
                                 capture_request=capture_request)
    assert_response(capture_response,
                    'http_metadata',
                    'reference',
                    'action_id',
                    '_links')


def test_should_full_capture_card_payment_idempotently(four_api):
    payment_response = make_card_payment(four_api)

    capture_request = CaptureRequest()
    capture_request.reference = new_uuid()
    capture_request.amount = 2

    idempotency_key = new_idempotency_key()

    capture_response_1 = retriable(callback=four_api.payments.capture_payment,
                                   payment_id=payment_response.id,
                                   capture_request=capture_request,
                                   idempotency_key=idempotency_key)
    assert_response(capture_response_1, 'action_id')

    capture_response_2 = retriable(callback=four_api.payments.capture_payment,
                                   payment_id=payment_response.id,
                                   capture_request=capture_request,
                                   idempotency_key=idempotency_key)
    assert_response(capture_response_2, 'action_id')

    assert capture_response_1.action_id == capture_response_2.action_id
