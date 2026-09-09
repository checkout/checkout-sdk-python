import pytest

from tests._assertions import assert_api_call
from checkout_sdk.balances.balances import BalancesQuery
from checkout_sdk.balances.balances_client import BalancesClient
from checkout_sdk.exception import CheckoutArgumentException


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return BalancesClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestBalancesClient:

    def test_should_retrieve_entity_balances(self, mocker, client: BalancesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = BalancesQuery()

        assert client.retrieve_entity_balances('entity_id', query) == 'response'
        assert_api_call(mock, 'balances/entity_id', query)

    def test_should_retrieve_top_up_instructions(self, mocker, client: BalancesClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.retrieve_top_up_instructions(
            'ent_w4jelhppmfiufdnatam37wrfc4', 'ca_g5y7d6jo4e2urgforcbf2ey5jm') == 'response'
        assert_api_call(
            mock,
            'entities/ent_w4jelhppmfiufdnatam37wrfc4/currency-accounts/'
            'ca_g5y7d6jo4e2urgforcbf2ey5jm/top-up-instructions')

    # Both values are interpolated straight into the path, so a blank one would build a malformed
    # URL. The guard must reject it before any request is made.
    @pytest.mark.parametrize('entity_id, currency_account_id, expected', [
        (None, 'ca_g5y7d6jo4e2urgforcbf2ey5jm', 'entity_id cannot be blank'),
        ('', 'ca_g5y7d6jo4e2urgforcbf2ey5jm', 'entity_id cannot be blank'),
        ('   ', 'ca_g5y7d6jo4e2urgforcbf2ey5jm', 'entity_id cannot be blank'),
        ('ent_w4jelhppmfiufdnatam37wrfc4', None, 'currency_account_id cannot be blank'),
        ('ent_w4jelhppmfiufdnatam37wrfc4', '', 'currency_account_id cannot be blank'),
        ('ent_w4jelhppmfiufdnatam37wrfc4', '   ', 'currency_account_id cannot be blank'),
    ])
    def test_should_reject_blank_path_parameters(self, mocker, client: BalancesClient,
                                                 entity_id, currency_account_id, expected):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        with pytest.raises(CheckoutArgumentException) as error:
            client.retrieve_top_up_instructions(entity_id, currency_account_id)

        assert str(error.value) == expected
        mock.assert_not_called()
