import pytest

from checkout_sdk.apm.sepa_client import SepaClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return SepaClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestSepaClient:

    def test_should_get_mandate(self, mocker, client: SepaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_mandate('mandate_id') == 'response'

    def test_should_cancel_mandate(self, mocker, client: SepaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.cancel_mandate('mandate_id') == 'response'

    def test_should_get_mandate_via_ppro(self, mocker, client: SepaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_mandate_via_ppro('mandate_id') == 'response'

    def test_should_cancel_mandate_via_ppro(self, mocker, client: SepaClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.post', return_value='response')
        assert client.cancel_mandate_via_ppro('payment_id') == 'response'
