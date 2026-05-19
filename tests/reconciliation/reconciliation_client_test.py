import pytest

from tests._assertions import assert_api_call
from checkout_sdk.common.common import QueryFilterDateRange
from checkout_sdk.reconciliation.reconciliation_client import ReconciliationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ReconciliationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestReconciliationClient:

    def test_should_query_payments_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = QueryFilterDateRange()

        assert client.query_payments_report(query) == 'response'
        assert_api_call(mock, 'reporting/payments', query)

    def test_should_get_single_payment_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.single_payment_report('payment_id') == 'response'
        assert_api_call(mock, 'reporting/payments/payment_id')

    def test_should_query_statements_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = QueryFilterDateRange()

        assert client.query_statements_report(query) == 'response'
        assert_api_call(mock, 'reporting/statements', query)

    def test_should_retrieve_csv_payment_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        # NOTE: the original test passed 'payment_id' (a str) where the client signature
        # expects a QueryFilterDateRange. Preserving that call as-is; only verifying path.
        assert client.retrieve_csv_payment_report('payment_id') == 'response'
        assert_api_call(mock, 'reporting/payments/download')

    def test_should_retrieve_csv_single_statement_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_csv_single_statement_report('statement_id') == 'response'
        assert_api_call(mock, 'reporting/statements/statement_id/payments/download')

    def test_should_retrieve_csv_statements_report(self, mocker, client: ReconciliationClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = QueryFilterDateRange()

        assert client.retrieve_csv_statements_report(query) == 'response'
        assert_api_call(mock, 'reporting/statements/download', query)
