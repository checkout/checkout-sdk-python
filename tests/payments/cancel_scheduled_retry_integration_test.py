from __future__ import absolute_import

import pytest

from checkout_sdk.payments.payments import CancelScheduledRetryRequest
from tests.checkout_test_utils import assert_response, new_idempotency_key
from tests.payments.payments_test_utils import make_card_payment


# tests
@pytest.mark.skip(reason='use cancel scheduled retry on demand, only works on payments with a pending scheduled retry')
def test_should_cancel_scheduled_retry(default_api, oauth_api):
    payment_response = make_card_payment(default_api)

    cancel_request = build_cancel_scheduled_retry_request(payment_response.reference)

    cancel_response = oauth_api.payments.cancel_scheduled_retry(payment_response.id, cancel_request)
    assert_cancel_scheduled_retry_response(cancel_response)


@pytest.mark.skip(reason='use cancel scheduled retry on demand, only works on payments with a pending scheduled retry')
def test_should_cancel_scheduled_retry_idempotently(default_api, oauth_api):
    payment_response = make_card_payment(default_api)

    cancel_request = build_cancel_scheduled_retry_request(payment_response.reference)
    idempotency_key = new_idempotency_key()

    cancel_response_1 = oauth_api.payments.cancel_scheduled_retry(payment_response.id, cancel_request, idempotency_key)
    assert_response(cancel_response_1)

    cancel_response_2 = oauth_api.payments.cancel_scheduled_retry(payment_response.id, cancel_request, idempotency_key)
    assert_response(cancel_response_2)

    assert cancel_response_1.action_id == cancel_response_2.action_id


# common methods

def build_cancel_scheduled_retry_request(reference: str) -> CancelScheduledRetryRequest:
    request = CancelScheduledRetryRequest()
    request.reference = reference
    return request


def assert_cancel_scheduled_retry_response(response):
    assert_response(response,
                    'http_metadata',
                    'reference',
                    'action_id',
                    '_links')
