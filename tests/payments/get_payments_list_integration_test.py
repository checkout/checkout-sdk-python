from datetime import datetime, timezone

from checkout_sdk.payments.payments import PaymentsQueryFilter
from tests.checkout_test_utils import assert_response, retriable
from tests.payments.payments_test_utils import make_card_payment


def test_should_get_payments_list(default_api):
    payment_response = make_card_payment(default_api, capture_on=datetime.now(timezone.utc))

    query = PaymentsQueryFilter()
    query.limit = 100
    query.skip = 0
    query.reference = payment_response.reference

    response = retriable(callback=default_api.payments.get_payments_list,
                         predicate=there_are_payments,
                         query=query)

    assert_response(response,
                    'http_metadata',
                    'limit',
                    'skip',
                    'total_count',
                    'data')

    assert payment_response.reference == response.data[0].reference


def there_are_payments(response) -> bool:
    return response.total_count is not None and response.total_count > 0
