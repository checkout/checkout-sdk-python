from __future__ import absolute_import

from tests.checkout_test_utils import assert_response, retriable
from tests.payments.previous.payments_previous_test_utils import make_card_payment


def test_should_get_payment_actions(previous_api):
    payment_response = make_card_payment(previous_api, capture=True)

    response = retriable(callback=previous_api.payments.get_payment_actions,
                         predicate=there_are_two_payment_actions,
                         payment_id=payment_response.id)

    actions = response.items
    assert type(actions) is list
    assert actions.__len__() > 0
    for action in actions:
        assert_response(action,
                        'amount',
                        'approved',
                        'processed_on',
                        'reference',
                        'response_code',
                        'response_summary',
                        'type')


def there_are_two_payment_actions(response) -> bool:
    return response.items.__len__() == 2
