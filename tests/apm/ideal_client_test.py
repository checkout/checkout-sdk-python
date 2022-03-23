import pytest

from checkout_sdk.apm.ideal_client import IdealClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IdealClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIdealClient:

    def test_should_get_info(self, mocker, client: IdealClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_info() == 'response'

    def test_get_issuers(self, mocker, client: IdealClient):
        mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')
        assert client.get_issuers() == 'response'
