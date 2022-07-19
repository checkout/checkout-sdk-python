import pytest

from checkout_sdk.forex.forex import QuoteRequest
from checkout_sdk.forex.forex_client import ForexClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ForexClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestForexClient:

    def test_should_request_quote(self, mocker, client: ForexClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.request_quote(QuoteRequest()) == 'response'
