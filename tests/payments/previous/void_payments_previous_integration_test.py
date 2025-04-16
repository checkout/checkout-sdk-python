from __future__ import absolute_import

import pytest

from checkout_sdk.payments.payments import VoidRequest
from tests.checkout_test_utils import new_uuid, assert_response, new_idempotency_key, retriable
from tests.payments.previous.payments_previous_test_utils import make_card_payment


@pytest.mark.skip(reason='not available')
def test_should_void_card_payment(previous_api):
    payment_response = make_card_payment(previous_api)

    void_request = VoidRequest()
    void_request.reference = new_uuid()

    void_response = retriable(callback=previous_api.payments.void_payment,
                              payment_id=payment_response.id,
                              void_request=void_request)
    assert_response(void_response,
                    'reference',
                    'action_id',
                    '_links')


@pytest.mark.skip(reason='not available')
def test_should_void_card_payment_idempotently(previous_api):
    payment_response = make_card_payment(previous_api)

    void_request = VoidRequest()
    void_request.reference = new_uuid()

    idempotency_key = new_idempotency_key()

    void_response_1 = retriable(callback=previous_api.payments.void_payment,
                                payment_id=payment_response.id,
                                void_request=void_request,
                                idempotency_key=idempotency_key)
    assert_response(void_response_1)

    void_response_2 = retriable(callback=previous_api.payments.void_payment,
                                payment_id=payment_response.id,
                                void_request=void_request,
                                idempotency_key=idempotency_key)
    assert_response(void_response_2)

    assert void_response_1.action_id == void_response_2.action_id
