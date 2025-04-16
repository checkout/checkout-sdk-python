import pytest

from checkout_sdk.payments.payments import PaymentsQueryFilter
from tests.checkout_test_utils import retriable, assert_response
from tests.payments.previous.payments_previous_test_utils import make_card_payment


@pytest.mark.skip(reason='not available')
def test_should_get_payments_list(previous_api):
    payment_response = make_card_payment(previous_api)

    query = PaymentsQueryFilter()
    query.limit = 100
    query.skip = 0
    query.reference = payment_response.reference

    response = retriable(callback=previous_api.payments.get_payments_list,
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
