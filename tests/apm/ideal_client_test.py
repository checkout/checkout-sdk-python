import pytest

from tests._assertions import assert_api_call
from checkout_sdk.apm.ideal_client import IdealClient


@pytest.fixture(scope='class')
def client(mock_sdk_configuration, mock_api_client):
    return IdealClient(api_client=mock_api_client, configuration=mock_sdk_configuration)


class TestIdealClient:

    def test_should_get_info(self, mocker, client: IdealClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_info() == 'response'
        assert_api_call(mock, 'ideal-external')

    def test_get_issuers(self, mocker, client: IdealClient):
        mock = mocker.patch('checkout_sdk.api_client.ApiClient.get', return_value='response')

        assert client.get_issuers() == 'response'
        assert_api_call(mock, 'ideal-external/issuers')
