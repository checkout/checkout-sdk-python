import pytest

from checkout_sdk.issuing.transactions import TransactionsQueryFilter
from tests.checkout_test_utils import assert_response


@pytest.mark.skip("Avoid creating cards all the time")
class TestTransactionsIssuing:
    # tests

    def test_should_get_list_transactions(self, issuing_checkout_api):
        query = TransactionsQueryFilter()

        response = issuing_checkout_api.issuing.get_list_transactions(query)

        assert_response(response,
                        'limit',
                        'skip',
                        'total_count',
                        'data')
        assert len(response.data) > 0

    def test_should_get_single_transaction(self, issuing_checkout_api):
        query = TransactionsQueryFilter()
        list_response = issuing_checkout_api.issuing.get_list_transactions(query)

        response = issuing_checkout_api.issuing.get_single_transaction(list_response.data[0].id)

        assert_response(response,
                        'id',
                        'created_on',
                        'status',
                        'transaction_type',
                        'client',
                        'entity',
                        'card',
                        'cardholder',
                        'amounts',
                        'merchant',
                        'messages')
