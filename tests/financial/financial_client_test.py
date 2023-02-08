import pytest

from checkout_sdk.financial.financial import FinancialActionsQuery
from checkout_sdk.financial.financial_client import FinancialClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return FinancialClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestFinancialClient:

    def test_should_query_financial_actions(self, mocker, client: FinancialClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.query(FinancialActionsQuery()) == 'response'
