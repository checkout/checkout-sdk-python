import pytest

from checkout_sdk.common.common import QueryFilterDateRange
from checkout_sdk.reconciliation.reconciliation_client import ReconciliationClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ReconciliationClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestReconciliationClient:

    def test_should_query_payments_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.query_payments_report(QueryFilterDateRange()) == 'response'

    def test_should_get_single_payment_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.single_payment_report('payment_id') == 'response'

    def test_should_query_statements_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.query_statements_report(QueryFilterDateRange()) == 'response'

    def test_should_retrieve_csv_payment_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_csv_payment_report('payment_id') == 'response'

    def test_should_retrieve_csv_single_statement_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_csv_single_statement_report('statement_id') == 'response'

    def test_should_retrieve_csv_statements_report(self, mocker, client: ReconciliationClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_csv_statements_report(QueryFilterDateRange()) == 'response'
