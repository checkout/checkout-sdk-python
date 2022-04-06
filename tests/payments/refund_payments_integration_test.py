from __future__ import absolute_import

from datetime import datetime, timezone

from checkout_sdk.payments.payments import RefundRequest
from tests.checkout_test_utils import new_uuid, assert_response, new_idempotency_key, retriable
from tests.payments.payments_test_utils import make_card_payment


def test_should_refund_card_payment(default_api):
    payment_response = make_card_payment(default_api, capture_on=datetime.now(timezone.utc))

    refund_request = RefundRequest()
    refund_request.reference = new_uuid()
    refund_request.amount = 2

    refund_response = retriable(callback=default_api.payments.refund_payment,
                                payment_id=payment_response.id,
                                refund_request=refund_request)

    assert_response(refund_response,
                    'reference',
                    'action_id',
                    '_links')


def test_should_refund_card_payment_idempotently(default_api):
    payment_response = make_card_payment(default_api, capture_on=datetime.now(timezone.utc))

    refund_request = RefundRequest()
    refund_request.reference = new_uuid()
    refund_request.amount = 1

    idempotency_key = new_idempotency_key()

    refund_response_1 = retriable(callback=default_api.payments.refund_payment,
                                  payment_id=payment_response.id,
                                  refund_request=refund_request,
                                  idempotency_key=idempotency_key)
    assert_response(refund_response_1)

    refund_response_2 = retriable(callback=default_api.payments.refund_payment,
                                  payment_id=payment_response.id,
                                  refund_request=refund_request,
                                  idempotency_key=idempotency_key)
    assert_response(refund_response_2)

    assert refund_response_1.action_id == refund_response_2.action_id
