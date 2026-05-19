from __future__ import absolute_import

from datetime import datetime, timezone, timedelta

import pytest

from checkout_sdk.payments.payments import PaymentsSearchRequest
from tests.checkout_test_utils import assert_response, retriable
from tests.payments.payments_test_utils import make_card_payment


# tests
@pytest.mark.skip(reason='use search payments when needed, skipped because of the time it takes to execute')
def test_should_search_payments(default_api, oauth_api):
    payment_response = make_card_payment(default_api)

    search_request = build_payments_search_request(payment_response.id)

    response = retriable(callback=oauth_api.payments.search_payments,
                         predicate=there_are_search_results,
                         timeout=5,
                         search_request=search_request)
    assert_search_response(response, payment_response.id)


# common methods

def build_payments_search_request(payment_id: str) -> PaymentsSearchRequest:
    request = PaymentsSearchRequest()
    request.query = "id:'" + payment_id + "'"
    request.limit = 10
    request.from_ = datetime.now(timezone.utc) - timedelta(minutes=5)
    request.to = datetime.now(timezone.utc) + timedelta(minutes=5)
    return request


def assert_search_response(response, payment_id: str):
    assert_response(response,
                    'http_metadata',
                    'data')
    assert response.data[0].id == payment_id


def there_are_search_results(response) -> bool:
    data = getattr(response, 'data', None)
    return data is not None and len(data) > 0
