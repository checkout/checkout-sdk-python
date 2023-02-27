from checkout_sdk.financial.financial import FinancialActionsQuery
from tests.checkout_test_utils import retriable, assert_response
from tests.payments.payments_test_utils import make_card_payment


def test_should_query_financial_actions(default_api, oauth_api):
    payment = make_card_payment(default_api, amount=100, capture=True)

    query = FinancialActionsQuery()
    query.payment_id = payment.id

    response = retriable(callback=oauth_api.financial.query,
                         predicate=there_are_financial_actions,
                         timeout=5,
                         query=query)

    assert_response(response,
                    'http_metadata',
                    'count',
                    'data',
                    '_links')

    if response.data:
        actions = response.data
        for action in actions:
            assert_response(action,
                            'payment_id',
                            'action_id',
                            'action_type',
                            'entity_id',
                            'currency_account_id',
                            'processed_on',
                            'requested_on')
            assert payment.id == action.payment_id


def there_are_financial_actions(response) -> bool:
    return response.count is not None and response.count > 0
