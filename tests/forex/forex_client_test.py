import pytest

from tests._assertions import assert_api_call
from checkout_sdk.forex.forex import QuoteRequest, RatesQueryFilter
from checkout_sdk.forex.forex_client import ForexClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return ForexClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestForexClient:

    def test_should_request_quote(self, mocker, client: ForexClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        body = QuoteRequest()

        assert client.request_quote(body) == 'response'
        assert_api_call(mock, 'forex/quotes', body)

    def test_should_get_rates(self, mocker, client: ForexClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        query = RatesQueryFilter()

        assert client.get_rates(query) == 'response'
        assert_api_call(mock, 'forex/rates', query)
