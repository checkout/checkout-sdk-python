import pytest

from checkout_sdk.networktokens.network_tokens import ProvisionNetworkTokenRequest, RequestCryptogramRequest, \
    DeleteNetworkTokenRequest
from checkout_sdk.networktokens.network_tokens_client import NetworkTokensClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return NetworkTokensClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestNetworkTokensClient:

    def test_provision_network_token(self, mocker, client: NetworkTokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.provision_network_token(ProvisionNetworkTokenRequest()) == 'response'

    def test_get_network_token(self, mocker, client: NetworkTokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_network_token('network_token_id') == 'response'

    def test_request_cryptogram(self, mocker, client: NetworkTokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_cryptogram('network_token_id', RequestCryptogramRequest()) == 'response'

    def test_delete_network_token(self, mocker, client: NetworkTokensClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.delete_network_token('network_token_id', DeleteNetworkTokenRequest()) == 'response'
