import pytest

from checkout_sdk.issuing.cardholders import CardholderRequest
from checkout_sdk.issuing.issuing_client import IssuingClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IssuingClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIssuingClient:

    def test_should_create_cardholder(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.create_cardholder(CardholderRequest()) == 'response'

    def test_should_get_cardholder(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_cardholder('cardholder_id') == 'response'

    def test_should_get_cardholder_cards(self, mocker, client: IssuingClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_cardholder_cards('cardholder_id') == 'response'
