import pytest

from tests._assertions import assert_api_call
from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.balances.balances_client import BalancesClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return BalancesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestBalancesClient:

    def test_should_retrieve_entity_balances(self, mocker, client: BalancesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = BalancesQuery()

        assert client.retrieve_entity_balances('entity_id', query) == 'response'
        assert_api_call(mock, 'balances/entity_id', query)
