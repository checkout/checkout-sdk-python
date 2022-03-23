import pytest

from checkout_sdk.files.files import FileRequest
from checkout_sdk.marketplace.marketplace import OnboardEntityRequest, MarketplacePaymentInstrument
from checkout_sdk.marketplace.marketplace_client import MarketplaceClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return MarketplaceClient(api_client=mock_api_client, files_client=mock_api_client,
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
