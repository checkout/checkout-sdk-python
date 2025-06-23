import pytest

from checkout_sdk.forward.forward import ForwardRequest
from checkout_sdk.forward.forward_client import ForwardClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ForwardClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestForexClient:

    def test_should_forward_request(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.forward_request(ForwardRequest()) == 'response'

    def test_should_get_forward_request(self, mocker, client: ForwardClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get('forward_id') == 'response'
