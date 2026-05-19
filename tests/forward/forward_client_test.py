import pytest

from tests._assertions import assert_api_call
from checkout_sdk.forward.forward import ForwardRequest, SecretRequest
from checkout_sdk.forward.forward_client import ForwardClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ForwardClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestForwardClient:

    def test_should_forward_request(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = ForwardRequest()

        assert client.forward_request(body) == 'response'
        assert_api_call(mock, 'forward', body)

    def test_should_get_forward_request(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get('forward_id') == 'response'
        assert_api_call(mock, 'forward/forward_id')

    def test_should_create_secret(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = SecretRequest()

        assert client.create_secret(body) == 'response'
        assert_api_call(mock, 'forward/secrets', body)

    def test_should_list_secrets(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.list_secrets() == 'response'
        assert_api_call(mock, 'forward/secrets')

    def test_should_update_secret(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.patch', return_value='response')
        body = SecretRequest()

        assert client.update_secret('secret_name', body) == 'response'
        assert_api_call(mock, 'forward/secrets/secret_name', body)

    def test_should_delete_secret(self, mocker, client: ForwardClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.delete', return_value='response')

        assert client.delete_secret('secret_name') == 'response'
        assert_api_call(mock, 'forward/secrets/secret_name')
