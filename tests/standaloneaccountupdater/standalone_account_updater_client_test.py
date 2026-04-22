import pytest

from checkout_sdk.standaloneaccountupdater.standalone_account_updater import GetUpdatedCardCredentialsRequest
from checkout_sdk.standaloneaccountupdater.standalone_account_updater_client import StandaloneAccountUpdaterClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return StandaloneAccountUpdaterClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestStandaloneAccountUpdaterClient:

    def test_should_get_updated_card_credentials(self, mocker, client: StandaloneAccountUpdaterClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.get_updated_card_credentials(GetUpdatedCardCredentialsRequest()) == 'response'
