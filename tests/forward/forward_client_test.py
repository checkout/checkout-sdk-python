import pytest

from checkout_sdk.forward.forward import ForwardRequest, SecretRequest
from checkout_sdk.forward.forward_client import ForwardClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ForwardClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestForwardClient:

    def test_should_forward_request(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.forward_request(ForwardRequest()) == 'response'

    def test_should_get_forward_request(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get('forward_id') == 'response'

    def test_should_create_secret(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_secret(SecretRequest()) == 'response'

    def test_should_list_secrets(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.list_secrets() == 'response'

    def test_should_update_secret(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        assert client.update_secret('secret_name', SecretRequest()) == 'response'

    def test_should_delete_secret(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')
        assert client.delete_secret('secret_name') == 'response'
