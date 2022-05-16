import pytest

from checkout_sdk.common.enums import Currency
from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, MarketplacePaymentInstrument, \
    CreateTransferRequest, BalancesQuery, UpdateScheduleRequest
from checkout_sdk.marketplace.marketplace_client import MarketplaceClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return MarketplaceClient(api_client=mock_api_client,
                             files_client=mock_api_client,
                             transfers_client=mock_api_client,
                             balances_client=mock_api_client,
                             configuration=mock_sdk_configuration)


class TestMarketplaceClient:

    def test_should_create_entity(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_entity(OnboardEntityRequest()) == 'response'

    def test_should_get_entity(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_entity('entity_id') == 'response'

    def test_should_update_entity(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_entity('entity_id', OnboardEntityRequest()) == 'response'

    def test_should_create_payment_instrument(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_payment_instrument('entity_id', MarketplacePaymentInstrument()) == 'response'

    def test_should_upload_file(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.submit_file', return_value='response')
        assert client.upload_file(FileRequest()) == 'response'

    def test_should_initiate_transfer_of_funds(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.initiate_transfer_of_funds(CreateTransferRequest(), 'idempotency_key') == 'response'

    def test_should_retrieve_entity_balances(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_entity_balances('entity_id', BalancesQuery()) == 'response'

    def test_should_update_payout_schedule(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.put', return_value='response')
        assert client.update_payout_schedule('entity_id', Currency.USD, UpdateScheduleRequest()) == 'response'

    def test_should_retrieve_payout_schedule(self, mocker, client: MarketplaceClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.retrieve_payout_schedule('entity_id') == 'response'
